# Architecture baseline

This is the v3 proposal's intended architecture, not a claim that every component is implemented.

## Four-stage decision loop

1. **ASK / ROUTE:** classify a request as historical SQL, what-if simulation, optimization, clarification or refusal.
2. **ANALYZE:** draft validated read-only SQL, apply semantic definitions, execute under database permissions and resource limits, select a chart and produce a grounded explanation. A code-based answer checker verifies numeric claims against returned values.
3. **SIMULATE:** extract bounded parameters and run the inventory digital twin with Monte Carlo simulation. Return percentile ranges and explicit assumptions.
4. **OPTIMIZE & RECOMMEND:** select tested objective/constraint templates, validate the structured specification, show a model card for manager approval, solve with code, then test every plan in the twin. Return trade-offs, binding constraints or an honest infeasibility result.

## Logical components

| Component | Responsibility |
|---|---|
| Data ingestion | Migrate WWI from SQL Server to the project PostgreSQL schema; clean and document transformations. |
| PostgreSQL | Store mapped products, sales, purchase orders, suppliers, lead times and stock-related records. Provide a restricted read-only analytics role. |
| Semantic layer | Maintain at least 15 business definitions, formulas, SQL fragments and examples. Mark stock-dependent measures such as fill rate, stockout and lost sales as simulation-only. |
| SQL pipeline | Structured SQL drafting, code-level validation, bounded execution, chart selection, grounded insight and numeric answer checking. |
| Forecasting and twin | Fit demand and lead-time behaviour using the first 70% of history; simulate policy and optimizer-plan modes; report Monte Carlo percentiles. |
| Optimizer | Select from a tested catalog; assemble LP/MILP models in Python using PuLP and HiGHS; never let the LLM write solver code. |
| API | FastAPI endpoints: `/ask`, `/simulate`, `/optimize`. Contracts precede implementation. |
| Web application | Next.js/React interface with chat, evidence panels, fan charts, sliders, scenario presets, model-card approval and decision memo export. |
| Governance and evaluation | Security tests, decision log, AI-use log, model limitations, evaluation sets, SME user testing and business case. |

## Data and inventory boundaries

- WWI is synthetic. It can demonstrate the pipeline and validation method; it cannot establish real-world predictive accuracy.
- Verify stock history can be reconstructed from transactions. Do not assume a holdings table is historical.
- Select one stock group and 3–5 sufficiently active products or product groups.
- Use one replenishment process and a lost-sales assumption in the core simulator. Backorders are an optional stretch switch only.
- Start each simulation from recorded stock on hand.
- Distinguish observed data, derived values, model outputs and assumed financial inputs in storage, API responses and UI labels.

## Twin parameters

- `demand_multiplier`
- `lead_time_multiplier`
- `reorder_point`
- `order_quantity`
- `safety_stock`

Effective reorder point = `reorder_point + safety_stock`. Bounds and clamp-or-reject rules must be documented and enforced in code.

## Validation requirements

1. **Calibration:** fit on the first 70% of history and evaluate on the held-out 30%; report demand error/WAPE, lead-time percentiles and limitations.
2. **Interval coverage:** report the share of held-out weeks whose actual demand falls inside the p5–p95 range, per product and overall.
3. **Policy backtest:** replay held-out demand against the recommended plan and current policy; compare fill rate and cost.

Every optimizer plan must also be run in twin plan mode and checked under uncertainty.

## Optimizer requirements

- Tested catalog of objectives and constraint modules, with documented units, bounds and provenance for every value.
- Deterministic and scenario-based models; the latter uses sample average approximation if retained in final scope.
- Manager-visible model card before solving.
- Explicit infeasibility handling; never silently relax constraints.
- Compare against current policy, EOQ, safety-stock formulas and a grid-search baseline.
- Report binding constraints, marginal values, cost-service trade-offs and uncertainty.

## Security and governance invariants

- SQL is read-only, single-statement SELECT only, restricted to allowed tables/columns, with row limits and timeouts.
- Parameter values and optimizer catalog selections are validated in code.
- The LLM cannot execute Python, write optimization models or change simulator logic.
- Unsupported, unsafe, ambiguous or impossible requests must be clarified or refused rather than guessed.
- Every recommendation is logged with its approval decision. A human approves every plan; no order is placed automatically.
- Never commit secrets or real customer personal data.
