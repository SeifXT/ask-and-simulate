"""Migrate Wide World Importers (SQL Server) into the project's PostgreSQL schema (task D2).

DRAFT for team review. Run AFTER applying d2_postgres_schema_draft.sql.

What it does
------------
1. Reads each WWI table from SQL Server (read-only SELECTs).
2. Loads it into PostgreSQL with COPY, inside ONE transaction (all or nothing).
   The script is re-runnable: it truncates the target tables first.
3. Flags the modelled products (is_modelled = true) and fills meta.data_provenance.
4. Reconciles the result against numbers from the D1 spike test and writes
   docs/d2-load-report.md. Exit code 1 if any check fails.
5. Optionally tests that the read-only role (ask_ro) really is read-only.

Configuration (environment variables or a local, untracked .env file)
--------------------------------------------------------------------
SQLSERVER_ODBC_CONN  e.g. DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;
                     DATABASE=WideWorldImporters;Trusted_Connection=yes;TrustServerCertificate=yes
PG_ADMIN_URL         e.g. postgresql://postgres:<password>@localhost:5432/ask_simulate
ASK_RO_URL           (optional) postgresql://ask_ro:<password>@localhost:5432/ask_simulate

Never commit real passwords. Column names below come from the WWI documentation;
if SQL Server reports an invalid column name, fix the query in EXTRACTS.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

BATCH_SIZE = 10_000
MODELLED_ITEMS = (191, 177, 199, 184, 193)  # top 5 by units sold in Packaging Materials (D1 rule)
REPORT_PATH = Path(os.environ.get("LOAD_REPORT_PATH", "docs/d2-load-report.md"))


@dataclass(frozen=True)
class Extract:
    target: str                  # schema.table in PostgreSQL
    columns: tuple[str, ...]     # target columns, in the order the SELECT returns them
    source_sql: str              # T-SQL SELECT; must not contain ORDER BY


# Load order matters: parents before children (foreign keys).
EXTRACTS: tuple[Extract, ...] = (
    Extract("core.suppliers", ("supplier_id", "supplier_name"),
            "SELECT SupplierID, SupplierName FROM Purchasing.Suppliers"),
    Extract("core.stock_groups", ("stock_group_id", "stock_group_name"),
            "SELECT StockGroupID, StockGroupName FROM Warehouse.StockGroups"),
    Extract("core.products",
            ("stock_item_id", "product_name", "supplier_id", "unit_price",
             "recommended_retail_price", "units_per_outer", "nominal_lead_time_days"),
            "SELECT StockItemID, StockItemName, SupplierID, UnitPrice, RecommendedRetailPrice, "
            "QuantityPerOuter, LeadTimeDays FROM Warehouse.StockItems"),
    Extract("core.product_stock_groups", ("stock_item_id", "stock_group_id"),
            "SELECT StockItemID, StockGroupID FROM Warehouse.StockItemStockGroups"),
    Extract("core.customers", ("customer_id", "customer_name", "customer_category"),
            "SELECT c.CustomerID, c.CustomerName, cc.CustomerCategoryName "
            "FROM Sales.Customers c "
            "LEFT JOIN Sales.CustomerCategories cc ON cc.CustomerCategoryID = c.CustomerCategoryID"),
    Extract("core.sales_orders",
            ("order_id", "customer_id", "order_date", "expected_delivery_date"),
            "SELECT OrderID, CustomerID, OrderDate, ExpectedDeliveryDate FROM Sales.Orders"),
    Extract("core.invoices",
            ("invoice_id", "order_id", "customer_id", "invoice_date", "confirmed_delivery_time"),
            "SELECT InvoiceID, OrderID, CustomerID, InvoiceDate, ConfirmedDeliveryTime FROM Sales.Invoices"),
    Extract("core.invoice_lines",
            ("invoice_line_id", "invoice_id", "stock_item_id", "quantity", "unit_price", "line_profit"),
            "SELECT InvoiceLineID, InvoiceID, StockItemID, Quantity, UnitPrice, LineProfit "
            "FROM Sales.InvoiceLines"),
    Extract("core.purchase_orders",
            ("purchase_order_id", "supplier_id", "order_date", "expected_delivery_date"),
            "SELECT PurchaseOrderID, SupplierID, OrderDate, ExpectedDeliveryDate "
            "FROM Purchasing.PurchaseOrders"),
    Extract("core.purchase_order_lines",
            ("purchase_order_line_id", "purchase_order_id", "stock_item_id", "ordered_outers",
             "received_outers", "last_receipt_date", "expected_unit_price_per_outer"),
            "SELECT PurchaseOrderLineID, PurchaseOrderID, StockItemID, OrderedOuters, ReceivedOuters, "
            "LastReceiptDate, ExpectedUnitPricePerOuter FROM Purchasing.PurchaseOrderLines"),
    # Stock ledger: staging only, for validation. NOT exposed to the SQL assistant.
    Extract("staging.stock_item_transactions",
            ("stock_item_transaction_id", "stock_item_id", "transaction_type_id",
             "occurred_at", "quantity"),
            "SELECT StockItemTransactionID, StockItemID, TransactionTypeID, "
            "TransactionOccurredWhen, Quantity FROM Warehouse.StockItemTransactions"),
    Extract("staging.stock_item_holdings",
            ("stock_item_id", "quantity_on_hand", "reorder_level", "target_stock_level"),
            "SELECT StockItemID, QuantityOnHand, ReorderLevel, TargetStockLevel "
            "FROM Warehouse.StockItemHoldings"),
)

CORE_TABLES_FOR_PROVENANCE = tuple(e.target for e in EXTRACTS if e.target.startswith("core."))
VIEWS = ("core.v_daily_demand", "core.v_weekly_demand", "core.v_lead_times", "core.v_delivery_performance")

# Numbers from the D1 spike test and earlier exploration. Confirm against SQL Server first.
EXPECTED_ROWS = {
    "core.sales_orders": 73_595,
    "core.invoices": 70_510,
    "core.purchase_orders": 2_074,
}
EXPECTED_UNITS = {191: 207_324, 177: 147_675, 199: 143_184, 184: 110_075, 193: 58_200}
EXPECTED_WEEKS = {177: 179, 184: 179, 191: 179, 193: 179, 199: 178, 204: 179}  # Sunday weeks


def load_env() -> None:
    try:
        from dotenv import load_dotenv  # optional
        load_dotenv()
    except ImportError:
        pass


def table_count(cur: Any, qualified: str) -> int:
    cur.execute(f"SELECT COUNT(*) FROM {qualified}")
    return int(cur.fetchone()[0])


def load_all(src_conn: Any, pg_conn: Any) -> list[dict[str, Any]]:
    """Copy every extract into PostgreSQL in one transaction. Returns per-table results."""
    results: list[dict[str, Any]] = []
    with pg_conn.cursor() as pg:
        targets = ", ".join(e.target for e in EXTRACTS)
        pg.execute(f"TRUNCATE {targets} RESTART IDENTITY CASCADE")  # makes the script re-runnable

        for ex in EXTRACTS:
            src = src_conn.cursor()
            src.execute(f"SELECT COUNT(*) FROM ({ex.source_sql}) AS t")
            source_rows = int(src.fetchone()[0])

            src.execute(ex.source_sql)
            cols = ", ".join(ex.columns)
            with pg.copy(f"COPY {ex.target} ({cols}) FROM STDIN") as copy:
                while True:
                    rows = src.fetchmany(BATCH_SIZE)
                    if not rows:
                        break
                    for row in rows:
                        copy.write_row(tuple(row))
            src.close()

            loaded_rows = table_count(pg, ex.target)
            results.append({"table": ex.target, "source_rows": source_rows,
                            "loaded_rows": loaded_rows, "ok": source_rows == loaded_rows})
            print(f"{ex.target:38s} source={source_rows:>9,} loaded={loaded_rows:>9,} "
                  f"{'OK' if source_rows == loaded_rows else 'MISMATCH'}")

        # Flag the modelled products (D1 decision).
        pg.execute("UPDATE core.products SET is_modelled = (stock_item_id = ANY(%s))",
                   (list(MODELLED_ITEMS),))

        # Provenance labels (the SQL assistant and UI read these).
        pg.execute("DELETE FROM meta.data_provenance")
        for table in CORE_TABLES_FOR_PROVENANCE:
            schema, name = table.split(".")
            pg.execute("INSERT INTO meta.data_provenance VALUES (%s, %s, 'wwi_synthetic', %s)",
                       (schema, name, "Wide World Importers sample data: synthetic, US-based"))
        for view in VIEWS:
            schema, name = view.split(".")
            pg.execute("INSERT INTO meta.data_provenance VALUES (%s, %s, 'derived', %s)",
                       (schema, name, "Derived from core tables"))
        for table in ("staging.stock_item_transactions", "staging.stock_item_holdings"):
            schema, name = table.split(".")
            pg.execute("INSERT INTO meta.data_provenance VALUES (%s, %s, 'wwi_synthetic', %s)",
                       (schema, name, "Stock ledger: unreliable, validation only, not exposed"))
    return results


def reconcile(pg_conn: Any, expected_rows: dict[str, int] = EXPECTED_ROWS,
              expected_units: dict[int, int] = EXPECTED_UNITS,
              expected_weeks: dict[int, int] = EXPECTED_WEEKS,
              expected_late: tuple[int, int] = (4_470, 70_426),
              expected_confirmed: int = 70_426,
              expected_lead: tuple[int, int, float, int] = (2_474, 1, 1.43, 3),
              expected_range: tuple[date, date] = (date(2013, 1, 1), date(2016, 5, 31)),
              ) -> list[tuple[str, Any, Any, bool]]:
    """Compare PostgreSQL results with the spike-test numbers. Returns (check, expected, actual, ok)."""
    checks: list[tuple[str, Any, Any, bool]] = []

    def add(name: str, expected: Any, actual: Any) -> None:
        checks.append((name, expected, actual, expected == actual))

    with pg_conn.cursor() as cur:
        for table, n in expected_rows.items():
            add(f"{table} rows", n, table_count(cur, table))

        cur.execute("SELECT COUNT(*) FROM core.invoices WHERE confirmed_delivery_time IS NOT NULL")
        add("invoices with confirmed delivery", expected_confirmed, cur.fetchone()[0])

        cur.execute("SELECT MIN(invoice_date), MAX(invoice_date) FROM core.invoices")
        add("invoice date range", expected_range, tuple(cur.fetchone()))

        cur.execute("SELECT COUNT(*) FILTER (WHERE is_late), COUNT(*) FROM core.v_delivery_performance")
        add("late deliveries / delivered orders", expected_late, tuple(cur.fetchone()))

        cur.execute("SELECT stock_item_id, SUM(quantity) FROM core.invoice_lines "
                    "WHERE stock_item_id = ANY(%s) GROUP BY stock_item_id", (list(expected_units),))
        actual_units = {int(i): int(q) for i, q in cur.fetchall()}
        for item, units in expected_units.items():
            add(f"units sold, item {item}", units, actual_units.get(item))

        cur.execute("SELECT stock_item_id, COUNT(*) FROM core.v_weekly_demand "
                    "WHERE stock_item_id = ANY(%s) GROUP BY stock_item_id", (list(expected_weeks),))
        actual_weeks = {int(i): int(w) for i, w in cur.fetchall()}
        for item, weeks in expected_weeks.items():
            add(f"weeks with sales (Sunday weeks), item {item}", weeks, actual_weeks.get(item))

        cur.execute("SELECT COUNT(*), MIN(lead_time_days), ROUND(AVG(lead_time_days), 2), MAX(lead_time_days) "
                    "FROM core.v_lead_times WHERE supplier_id = 7")
        n, lo, avg, hi = cur.fetchone()
        add("supplier 7 lead times (n, min, avg, max)", expected_lead, (n, lo, float(avg), hi))

        cur.execute("SELECT COUNT(*) FROM core.products WHERE is_modelled")
        add("modelled products flagged", len(MODELLED_ITEMS), cur.fetchone()[0])
    return checks


def role_checks(ask_ro_url: str) -> list[tuple[str, Any, Any, bool]]:
    """The read-only role must read core and nothing else, and must not write."""
    import psycopg

    def attempt(sql: str) -> str:
        try:
            with psycopg.connect(ask_ro_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    if cur.description:
                        cur.fetchall()
                conn.rollback()
            return "allowed"
        except psycopg.Error:
            return "blocked"

    tests = [
        ("ask_ro can SELECT core.products", "SELECT * FROM core.products LIMIT 1", "allowed"),
        ("ask_ro cannot INSERT into core", "INSERT INTO core.suppliers VALUES (-1, 'x')", "blocked"),
        ("ask_ro cannot UPDATE core", "UPDATE core.products SET product_name = 'x'", "blocked"),
        ("ask_ro cannot DELETE from core", "DELETE FROM core.suppliers", "blocked"),
        ("ask_ro cannot read staging", "SELECT * FROM staging.stock_item_holdings", "blocked"),
        ("ask_ro cannot read assumptions", "SELECT * FROM assumptions.cost_inputs", "blocked"),
        ("ask_ro cannot read meta", "SELECT * FROM meta.project_settings", "blocked"),
    ]
    return [(name, want, attempt(sql), attempt(sql) == want) for name, sql, want in tests]


def write_report(load: list[dict[str, Any]], checks: list[tuple[str, Any, Any, bool]],
                 role: list[tuple[str, Any, Any, bool]]) -> None:
    lines = ["# D2 load report", "",
             "Generated by `migrate_wwi_to_postgres.py`. WWI is synthetic, US-based sample data.", "",
             "## Row counts (SQL Server source vs PostgreSQL)", "",
             "| Table | Source rows | Loaded rows | Result |", "| --- | ---: | ---: | --- |"]
    lines += [f"| {r['table']} | {r['source_rows']:,} | {r['loaded_rows']:,} | {'OK' if r['ok'] else 'MISMATCH'} |"
              for r in load]
    lines += ["", "## Reconciliation checks", "", "| Check | Expected | Actual | Result |", "| --- | --- | --- | --- |"]
    lines += [f"| {n} | {e} | {a} | {'PASS' if ok else 'FAIL'} |" for n, e, a, ok in checks]
    if role:
        lines += ["", "## Read-only role checks", "", "| Check | Expected | Actual | Result |", "| --- | --- | --- | --- |"]
        lines += [f"| {n} | {e} | {a} | {'PASS' if ok else 'FAIL'} |" for n, e, a, ok in role]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    load_env()
    import psycopg
    import pyodbc

    src_conn = pyodbc.connect(os.environ["SQLSERVER_ODBC_CONN"], readonly=True)
    with psycopg.connect(os.environ["PG_ADMIN_URL"]) as pg_conn:  # commits on success, rolls back on error
        load = load_all(src_conn, pg_conn)
    src_conn.close()

    with psycopg.connect(os.environ["PG_ADMIN_URL"]) as pg_conn:
        checks = reconcile(pg_conn)

    role = role_checks(os.environ["ASK_RO_URL"]) if os.environ.get("ASK_RO_URL") else []

    write_report(load, checks, role)
    for name, expected, actual, ok in checks + role:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: expected {expected}, got {actual}")
    all_ok = all(r["ok"] for r in load) and all(c[3] for c in checks + role)
    print("\nALL CHECKS PASSED" if all_ok else "\nSOME CHECKS FAILED: see the report and investigate before marking D2 done")
    print(f"Report written to {REPORT_PATH}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
