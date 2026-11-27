# D1: Wide World Importers spike-test results

**Decision: CONDITIONAL GO** (proposed; team to confirm and date it below)
**Dataset:** Microsoft Wide World Importers (OLTP), restored in SQL Server. Not yet migrated to PostgreSQL (task D2).
**Caveat to keep in the report:** WWI is a synthetic, US-based sample database. Results validate the method, not accuracy on real business data.

## Criteria (written before running the queries)

| # | Criterion | Evidence | Result |
| --- | --- | --- | --- |
| C1 | Stock history can be rebuilt, or an opening stock is assumed honestly | Receipts far exceed sales for every item checked (item 184: receipts 103x issues; 193: 431x; 204: 508x). Current holdings are not historical stock levels. Stock cannot be rebuilt from transactions. | PASS WITH ASSUMPTION: the twin starts from an assumed opening stock |
| C2 | At least 3 products in one stock group with sales in >= 80% of weeks | All six Packaging Materials items (177, 184, 191, 193, 199, 204) have sales in 178 to 179 of 179 weeks | PASS |
| C3 | At least 30 received purchase-order lines, with variation | Supplier-level: Litware, Inc. (supplier 7) supplies all six items and has 2,474 received lines. Lead time (order date to last receipt): min 1, average 1.43, max 3 days. Product-level counts vary (184: 566; 193: 896; 204: 932; 177: 2; 191: 1; 199: 9), so lead times are pooled at supplier level. | PASS (pooled at supplier level; variation is small) |
| C4 | Delivery timestamps usable for late-delivery questions | 70,426 of 70,510 invoices have a confirmed delivery time. 4,470 of 70,426 delivered orders (6.3%) arrived after the expected date. | PASS |
| C5 | At least 40 test weeks in a 70/30 split | Data runs 2013-01-01 to 2016-05-31. Split date 2015-05-23 leaves 54 test weeks. | PASS |

## Proposed stock group and products

- **Stock group:** Packaging Materials
- **Rule (set before checking weekly density):** the top 5 items by total units sold within the group.
- **Products:** 191 (Fragile despatch tape, 207,324 units), 177 (Shipping carton 413x285x187mm, 147,675), 199 (Heavy despatch tape, 143,184), 184 (Shipping carton 305x305x305mm, 110,075), 193 (Glass with care despatch tape, 58,200)
- **Reserve:** 204 (Tape dispenser, 23,634 units)

## Modelling assumptions to record

1. **Opening stock** is assumed, because historical stock cannot be rebuilt (C1).
2. **Lead times are pooled at supplier level** (Litware, Inc., all products): one empirical distribution of 1, 2 and 3 days, applied to every product. A supplier-delay scenario therefore affects all products together, which is realistic for a single supplier.
3. **The "current policy" baseline is an assumption**, not taken from the purchase history, which is unrealistic.
4. **Stress scenario:** the stored nominal lead time of 14 days is used as a labelled stress case, since observed lead times (1 to 3 days) are unrealistically short.

## Other caveats

1. **Purchase receipts** were generated independently of sales. Do not treat them as real replenishment behaviour.
2. **Units:** purchase quantities are in outers (item 184: 25 units per outer). Convert before comparing with sales.
3. **Stock groups overlap:** the same item can belong to several groups (the t-shirts appear in Clothing, Computing Novelties and T-Shirts). Summing by stock group can double count; document this in the semantic layer.
4. **Lead-time calibration will look easy** because the data is so regular. Say so in the report.
5. **SQL Server edition:** the installed edition is an Evaluation edition, which expires. Migrate the data to PostgreSQL early, or install the free Developer edition.

## Fallback if WWI is later rejected

DataCo Smart Supply Chain (Mendeley, CC BY 4.0). Name confirmed by: ________

## Sign-off

Decided by: ________  Date: ________
