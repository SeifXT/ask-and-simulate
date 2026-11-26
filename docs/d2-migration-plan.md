# D2 / D3 draft: WWI to PostgreSQL migration plan

**Status:** DRAFT for team review. Companion file: `d2_postgres_schema_draft.sql`.
**Reminder:** WWI is synthetic and US-based. Label it that way everywhere.

## 1. Decisions (settled by the team)

| # | Decision | Recommendation | Why |
| --- | --- | --- | --- |
| 1 | Load all products and history, or only the 5 chosen products? | **DECIDED: load ALL products and history; flag the 5 with `is_modelled = true`** | The SQL assistant needs categories, customers and late deliveries to answer realistic questions. The twin and optimizer only use the flagged products. It is about 700k rows, small for PostgreSQL. |
| 2 | Can the SQL assistant read the `assumptions` schema? | **DECIDED: no for now** | Keeps assumed values out of "observed" answers. Add a labelled view later if needed. |
| 3 | Weekly buckets | **DECIDED: weeks start on Sunday** | Matches Egypt and the SQL Server spike test, so weekly counts should reconcile exactly. |
| 4 | Keep `nominal_lead_time_days` in `core.products`? | **DECIDED: yes**, labelled as "stored, not observed" in the semantic layer | Needed for the 14-day stress scenario, but must never be mistaken for observed lead time. |

## 2. Mapping: WWI source to project table

Column names come from the WWI documentation. **Verify each against the restored database before writing the ETL.**

| WWI source | Project table | Columns kept |
| --- | --- | --- |
| Purchasing.Suppliers | core.suppliers | SupplierID, SupplierName |
| Warehouse.StockGroups | core.stock_groups | StockGroupID, StockGroupName |
| Warehouse.StockItems | core.products | StockItemID, StockItemName, SupplierID, UnitPrice, RecommendedRetailPrice, QuantityPerOuter, LeadTimeDays; plus `is_modelled` |
| Warehouse.StockItemStockGroups | core.product_stock_groups | StockItemID, StockGroupID |
| Sales.Customers + Sales.CustomerCategories | core.customers | CustomerID, CustomerName, category name |
| Sales.Orders | core.sales_orders | OrderID, CustomerID, OrderDate, ExpectedDeliveryDate |
| Sales.Invoices | core.invoices | InvoiceID, OrderID, CustomerID, InvoiceDate, ConfirmedDeliveryTime |
| Sales.InvoiceLines | core.invoice_lines | InvoiceLineID, InvoiceID, StockItemID, Quantity, UnitPrice, LineProfit |
| Purchasing.PurchaseOrders | core.purchase_orders | PurchaseOrderID, SupplierID, OrderDate, ExpectedDeliveryDate |
| Purchasing.PurchaseOrderLines | core.purchase_order_lines | PurchaseOrderLineID, PurchaseOrderID, StockItemID, OrderedOuters, ReceivedOuters, LastReceiptDate, ExpectedUnitPricePerOuter |

**Deliberately excluded from `core`:**
- `Warehouse.StockItemTransactions` and `Warehouse.StockItemHoldings`: stock history can't be rebuilt, so these go to `staging` only, for validation. The SQL assistant must not answer stock-level questions from them.
- `Sales.OrderLines`: redundant with invoice lines for demand.
- Cold-room temperature, vehicle tracking, people and application tables: not needed.

## 3. Modelled products

`is_modelled = true` for item IDs **191, 177, 199, 184, 193** (top 5 by units sold in Packaging Materials, rule fixed in D1). Item 204 is the reserve. Lead times are pooled at supplier level (supplier 7, Litware, Inc.).

## 4. Migration steps (re-runnable)

1. Install PostgreSQL for Windows (with pgAdmin) and create a database `ask_simulate`. Install the free SQL Server Developer edition, or migrate before the Evaluation edition expires.
2. Run `d2_postgres_schema_draft.sql` as an administrator. Replace the placeholder role password locally.
3. Write one Python script (Python 3.11+, `pandas`, `pyodbc` or `SQLAlchemy`, `psycopg`) that reads each WWI table, loads it into `staging`, then copies into `core` with the right types. Needs the "ODBC Driver 18 for SQL Server". Fallback: export tables to CSV from SSMS and load with PostgreSQL `COPY`.
4. Set `is_modelled` for the five products, and fill `meta.data_provenance` (all `core` tables: `wwi_synthetic`; views: `derived`; `assumptions` tables: `assumed` or `sourced`).
5. Write a short cleaning log: every cast, rule and row count. WWI is clean, so expect few or no dropped rows. State that.
6. Run the acceptance checks below. Do not mark D2 done until all pass.

## 5. Acceptance checks (reconcile PostgreSQL against SQL Server)

Numbers below come from the D1 spike test and the earlier exploration. **Confirm each against SQL Server first.**

| Check | Expected |
| --- | --- |
| `core.sales_orders` rows | 73,595 |
| `core.invoices` rows / with confirmed delivery | 70,510 / 70,426 |
| `core.purchase_orders` rows | 2,074 |
| Date range | 2013-01-01 to 2016-05-31 |
| Late deliveries in `v_delivery_performance` | 4,470 of 70,426 |
| Total units sold: item 191 / 177 / 199 / 184 / 193 | 207,324 / 147,675 / 143,184 / 110,075 / 58,200 |
| Supplier 7 lead times in `v_lead_times` | 2,474 lines; min 1, average 1.43, max 3 |
| Weeks with sales per modelled item | 178 to 179 (Sunday weeks, should match the spike test exactly) |
| `ask_ro` can SELECT from `core` | yes |
| `ask_ro` can INSERT, UPDATE, DELETE, or read `staging`, `assumptions`, `app` | no (these are your first security tests) |

## 6. Risks

- Column names are unverified until the ETL runs.
- The SQL Server Evaluation edition expires: finish the migration early.
- Purchase quantities are in **outers**: always convert before comparing with sales.
- Items in multiple stock groups can be double counted when summing by group.
