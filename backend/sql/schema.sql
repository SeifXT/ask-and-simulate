/* =====================================================================
   Ask & Simulate: DRAFT PostgreSQL schema (tasks D2 / D3)
   Status: DRAFT for team review. Not yet run.

   Source: Microsoft Wide World Importers (WWI), a SYNTHETIC US-based
   sample database. Column names are mapped from the WWI documentation;
   verify each one against the restored SQL Server database in D2.

   Design rules (from PROJECT_CONTEXT.md):
   - Observed (synthetic) data, derived values and assumptions live in
     SEPARATE schemas and are labelled.
   - The SQL assistant can read only the "core" schema, through a
     read-only role. Stock ledger tables are deliberately NOT loaded
     into core, because WWI's stock history is unreliable and must not be
     presented as observed history.
   - Never commit real passwords. Placeholders below must be replaced
     locally and kept in an untracked .env file.
   ===================================================================== */

CREATE SCHEMA IF NOT EXISTS staging;      -- raw copies of WWI tables; never exposed to the SQL assistant
CREATE SCHEMA IF NOT EXISTS core;         -- cleaned WWI-derived data (synthetic); read-only for the SQL assistant
CREATE SCHEMA IF NOT EXISTS assumptions;  -- labelled sourced/assumed values: EGP costs, opening stock, baseline policy
CREATE SCHEMA IF NOT EXISTS meta;         -- provenance labels and project settings
CREATE SCHEMA IF NOT EXISTS app;          -- application logs, written by the backend only (tables added later)

/* ---------- staging: stock ledger copies, for validation only ---------- */
-- Stock history cannot be rebuilt from these (receipts were generated independently of sales).
-- They are NOT in core and the SQL assistant cannot read them.

CREATE TABLE staging.stock_item_transactions (
    stock_item_transaction_id  integer PRIMARY KEY,
    stock_item_id              integer NOT NULL,
    transaction_type_id        integer NOT NULL,
    occurred_at                timestamp NOT NULL,
    quantity                   numeric(18,3) NOT NULL
);

CREATE TABLE staging.stock_item_holdings (
    stock_item_id       integer PRIMARY KEY,
    quantity_on_hand    integer,
    reorder_level       integer,
    target_stock_level  integer
);

/* ---------- core: reference data ---------- */

CREATE TABLE core.suppliers (
    supplier_id    integer PRIMARY KEY,
    supplier_name  text NOT NULL
);

CREATE TABLE core.stock_groups (
    stock_group_id    integer PRIMARY KEY,
    stock_group_name  text NOT NULL
);

CREATE TABLE core.products (
    stock_item_id             integer PRIMARY KEY,
    product_name              text NOT NULL,
    supplier_id               integer NOT NULL REFERENCES core.suppliers (supplier_id),
    unit_price                numeric(18,2) NOT NULL,
    recommended_retail_price  numeric(18,2),
    units_per_outer           integer NOT NULL,   -- purchase quantities are in outers
    nominal_lead_time_days    integer,            -- value STORED in WWI; NOT an observed lead time
    is_modelled               boolean NOT NULL DEFAULT false  -- true only for the products used by the twin and optimizer
);

-- Items can belong to several stock groups (e.g. t-shirts are in 3 groups).
-- Summing by stock group can double count: see the semantic layer (D4).
CREATE TABLE core.product_stock_groups (
    stock_item_id   integer NOT NULL REFERENCES core.products (stock_item_id),
    stock_group_id  integer NOT NULL REFERENCES core.stock_groups (stock_group_id),
    PRIMARY KEY (stock_item_id, stock_group_id)
);

CREATE TABLE core.customers (
    customer_id        integer PRIMARY KEY,
    customer_name      text NOT NULL,
    customer_category  text
);

/* ---------- core: sales ---------- */

CREATE TABLE core.sales_orders (
    order_id                integer PRIMARY KEY,
    customer_id             integer NOT NULL REFERENCES core.customers (customer_id),
    order_date              date NOT NULL,
    expected_delivery_date  date
);

CREATE TABLE core.invoices (
    invoice_id               integer PRIMARY KEY,
    order_id                 integer REFERENCES core.sales_orders (order_id),
    customer_id              integer NOT NULL REFERENCES core.customers (customer_id),
    invoice_date             date NOT NULL,
    confirmed_delivery_time  timestamp
);

CREATE TABLE core.invoice_lines (
    invoice_line_id  integer PRIMARY KEY,
    invoice_id       integer NOT NULL REFERENCES core.invoices (invoice_id),
    stock_item_id    integer NOT NULL REFERENCES core.products (stock_item_id),
    quantity         integer NOT NULL,          -- units sold (this is the demand signal)
    unit_price       numeric(18,2) NOT NULL,
    line_profit      numeric(18,2)
);

/* ---------- core: purchasing ---------- */

CREATE TABLE core.purchase_orders (
    purchase_order_id       integer PRIMARY KEY,
    supplier_id             integer NOT NULL REFERENCES core.suppliers (supplier_id),
    order_date              date NOT NULL,
    expected_delivery_date  date
);

CREATE TABLE core.purchase_order_lines (
    purchase_order_line_id         integer PRIMARY KEY,
    purchase_order_id              integer NOT NULL REFERENCES core.purchase_orders (purchase_order_id),
    stock_item_id                  integer NOT NULL REFERENCES core.products (stock_item_id),
    ordered_outers                 integer NOT NULL,   -- in OUTERS, multiply by units_per_outer for units
    received_outers                integer,
    last_receipt_date              date,
    expected_unit_price_per_outer  numeric(18,2)
);

/* ---------- core: derived views (what the twin and SQL assistant use) ---------- */

CREATE VIEW core.v_daily_demand AS
SELECT il.stock_item_id,
       i.invoice_date AS demand_date,
       SUM(il.quantity) AS units_sold
FROM core.invoice_lines il
JOIN core.invoices i ON i.invoice_id = il.invoice_id
GROUP BY il.stock_item_id, i.invoice_date;

-- Weeks START ON SUNDAY (team decision; matches Egypt and the D1 spike test, where
-- SQL Server's DATEDIFF(week) counts Sunday boundaries). EXTRACT(DOW) gives 0 for Sunday.
CREATE VIEW core.v_weekly_demand AS
SELECT stock_item_id,
       (demand_date - EXTRACT(DOW FROM demand_date)::int) AS week_start,
       SUM(units_sold) AS units_sold
FROM core.v_daily_demand
GROUP BY stock_item_id, (demand_date - EXTRACT(DOW FROM demand_date)::int);

CREATE VIEW core.v_lead_times AS
SELECT pol.purchase_order_line_id,
       po.supplier_id,
       pol.stock_item_id,
       po.order_date,
       pol.last_receipt_date,
       (pol.last_receipt_date - po.order_date) AS lead_time_days   -- OBSERVED, whole days
FROM core.purchase_order_lines pol
JOIN core.purchase_orders po ON po.purchase_order_id = pol.purchase_order_id
WHERE pol.last_receipt_date IS NOT NULL;

CREATE VIEW core.v_delivery_performance AS
SELECT o.order_id,
       o.customer_id,
       o.order_date,
       o.expected_delivery_date,
       i.confirmed_delivery_time::date AS confirmed_delivery_date,
       (i.confirmed_delivery_time::date - o.expected_delivery_date) AS days_late,
       (i.confirmed_delivery_time::date > o.expected_delivery_date) AS is_late
FROM core.sales_orders o
JOIN core.invoices i ON i.order_id = o.order_id
WHERE i.confirmed_delivery_time IS NOT NULL;

/* ---------- assumptions: every value labelled sourced or assumed ---------- */

CREATE TABLE assumptions.cost_inputs (
    input_id             serial PRIMARY KEY,
    input_name           text NOT NULL,     -- e.g. holding_cost_rate_per_year, ordering_cost_per_order
    value                numeric(18,4) NOT NULL,
    unit                 text NOT NULL,
    currency             text NOT NULL DEFAULT 'EGP',
    classification       text NOT NULL CHECK (classification IN ('sourced', 'assumed')),
    source_or_rationale  text NOT NULL,
    date_checked         date NOT NULL,
    owner                text NOT NULL
);

-- WWI's stock history cannot be rebuilt, so the twin starts from an assumed opening stock.
CREATE TABLE assumptions.opening_stock (
    stock_item_id  integer PRIMARY KEY REFERENCES core.products (stock_item_id),
    units          integer NOT NULL,
    rationale      text NOT NULL
);

-- The "current policy" baseline is an assumption, not taken from WWI purchase history.
CREATE TABLE assumptions.baseline_policy (
    stock_item_id  integer PRIMARY KEY REFERENCES core.products (stock_item_id),
    reorder_point  integer NOT NULL,
    order_units    integer NOT NULL,
    rationale      text NOT NULL
);

/* ---------- meta: provenance and settings ---------- */

CREATE TABLE meta.data_provenance (
    schema_name  text NOT NULL,
    table_name   text NOT NULL,
    origin       text NOT NULL CHECK (origin IN ('wwi_synthetic', 'derived', 'assumed', 'sourced')),
    note         text,
    PRIMARY KEY (schema_name, table_name)
);

CREATE TABLE meta.project_settings (
    setting_key  text PRIMARY KEY,
    setting_value text NOT NULL,
    note         text
);

INSERT INTO meta.project_settings (setting_key, setting_value, note) VALUES
  ('train_test_split_date', '2015-05-23', '70/30 chronological split from the D1 spike test; 54 test weeks'),
  ('supplier_for_lead_time_pooling', '7', 'Litware, Inc., supplies all candidate products; lead times pooled at supplier level');

/* ---------- roles: the SQL assistant gets read-only access to core only ---------- */

-- Run as an administrator. Replace the placeholder locally; never commit a real password.
CREATE ROLE ask_ro LOGIN PASSWORD 'CHANGE_ME_LOCALLY';
ALTER ROLE ask_ro SET default_transaction_read_only = on;
ALTER ROLE ask_ro SET statement_timeout = '5s';

REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA core TO ask_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA core TO ask_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA core GRANT SELECT ON TABLES TO ask_ro;

-- Row limits cannot be set per role in PostgreSQL: the SQL validator (D6) must add a LIMIT.
-- The validator's table/column allowlist is an additional layer on top of these permissions.
