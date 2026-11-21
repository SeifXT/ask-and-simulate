# Data, provenance and assumptions register

Use this register before implementing data-dependent features. Do not fill unknown values with guesses.

## Dataset

- **Primary source:** Microsoft Wide World Importers sample database.
- **Nature:** synthetic wholesale/importer sample data.
- **Licence:** the proposal records an MIT licence; verify the applicable source distribution and retain its notice.
- **Migration:** SQL Server source to project-owned PostgreSQL schema.
- **Scope:** one stock group and 3–5 high-volume products or product groups.
- **Spike-test evidence:** row counts, date ranges, missingness/gaps, reconstructable stock history, product sales density, supplier lead-time availability, delivery timestamps and a 70/30 split.

## Data provenance table

| Field / metric | Source | Observed / derived / assumed | Transformation / formula | Verified by |
|---|---|---|---|---|
| Product | To be completed after WWI spike test | Observed | Document mapping | |
| Sales demand | To be completed after WWI spike test | Observed/derived | Document aggregation and date grain | |
| Supplier lead time | Purchase order and receipt records, subject to verification | Derived | Receipt date minus order date | |
| Stock on hand | Reconstructed from stock transactions if possible | Derived | Document opening balance and transaction logic | |
| Unit cost / margin | SME interviews or public figures | Sourced or assumed | Record source and date | |
| Budget / capacity / supplier terms | SME interviews or labelled assumptions | Sourced or assumed | Record units and bounds | |
| FX depreciation scenario | Public figure or explicit scenario assumption | Sourced or assumed | Record baseline and shock | |

## Interpretation rules

- The dataset is synthetic and US-based. The EGP cost layer does not make the operational dataset Egyptian.
- Do not claim observed historical stockouts or lost sales if the source does not record them.
- Fill rate, stockout and lost-sales metrics are simulation-only unless verified observed data supports them.
- Clearly distinguish observed data, derived values, model outputs and assumptions.
- Avoid double-counting lost revenue and lost margin.

## Assumption register template

| ID | Input | Value | Unit | Classification (sourced/assumption) | Source / rationale | Date checked | Owner |
|---|---|---:|---|---|---|---|---|
| A-001 | | | | | | | |
