# Supervisor review brief — Ask & Simulate v3

**Purpose:** Obtain written supervisor approval of the updated v3 project scope and draft evaluation targets before reporting experimental results.
**Status:** For supervisor review. No approval is implied by this document.

## 1. Updated project scope

Ask & Simulate is a natural-language decision-support system for inventory and replenishment decisions. It routes manager questions to three controlled capabilities:

1. **Historical analysis:** natural-language questions translated into validated, read-only SQL against PostgreSQL, with grounded explanations and evidence.
2. **Inventory simulation:** a Monte Carlo inventory digital twin for bounded what-if scenarios involving demand, lead time and replenishment policy.
3. **Optimization:** a template-based LP/MILP engine using a tested objective/constraint catalog, with model-card review and manager approval. Every proposed plan is evaluated in the digital twin before it is recommended.

### Dataset and business context

- Primary dataset: Microsoft Wide World Importers (WWI), a synthetic wholesale/importer sample database.
- Data migration: SQL Server to a project-owned PostgreSQL schema.
- Business layer: Egyptian cost and operating assumptions expressed in EGP. Each value will be labelled as sourced or assumed and documented with provenance.
- Initial inventory scope: one stock group and 3–5 high-volume products or product groups, subject to the WWI data spike test.

### Validation approach

The project will evaluate three distinct parts:

- **Calibration:** fit demand and lead-time behaviour on the first 70% of the chronological history and evaluate on the held-out 30%.
- **Prediction interval coverage:** measure how often actual held-out weekly demand falls inside the model's p5–p95 interval.
- **Policy backtesting:** compare the recommended replenishment policy with the current policy on held-out demand, using service and cost measures supported by the data/simulation.

### Safety and decision governance

- SQL execution is read-only and constrained by code-level validation, table/column allowlists, row limits and timeouts.
- Deterministic code performs calculations, simulation and optimization-model construction; the LLM interprets requests and explains verified outputs.
- Every optimization proposal is shown for human approval; the system does not place orders automatically.
- Synthetic dataset observations, derived values, model outputs and EGP assumptions will be distinguished explicitly.

## 2. Draft evaluation targets for supervisor agreement

These are proposed targets, not achieved results. They must be agreed before evaluation results are presented.

| Measure | Proposed target | Measurement definition / clarification |
|---|---:|---|
| SQL execution accuracy | >= 80% | Define a test case as correct only when the generated query executes safely and returns the expected result for the question. Confirm denominator and treatment of safe refusals. |
| Router accuracy | >= 90% | Correct routing across historical SQL, simulation, optimization, clarification and refusal cases. Confirm class balance and test-set size. |
| Parameter extraction accuracy | >= 85% | Correct extraction of required simulation/optimization inputs against labelled test cases. Define exact-match versus tolerance-based scoring. |
| p5–p95 interval coverage | 85–95% | Share of held-out product-weeks where actual demand falls inside the predicted p5–p95 interval. Report per product and overall. |
| Calibration error | TBD with supervisor | Agree metric, aggregation and acceptable threshold after inspecting WWI data and baseline behaviour. |
| Optimizer stability | TBD with supervisor | Agree what constitutes stability (e.g. feasibility, repeatability under fixed inputs/seeds, and sensitivity under small input changes). |
| Task-time reduction | TBD with supervisor | Agree baseline task, comparison method, participant/sample size and target reduction. |

## 3. Questions requiring supervisor confirmation

1. Is the updated v3 scope and the WWI dataset with an Egyptian EGP cost layer acceptable?
2. Is the template-based LP/MILP optimizer, validated through the inventory twin and requiring human approval, acceptable?
3. Are the three validation components (calibration, p5–p95 coverage and policy backtesting) appropriate?
4. Are the proposed SQL execution, router, extraction and interval-coverage targets acceptable?
5. What definitions and thresholds should be used for calibration error, optimizer stability and task-time reduction?
6. Are there any required changes to the scope, evaluation methodology or deliverables?

## 4. Sign-off record

Complete only after receiving the supervisor's response.

- Supervisor name: TBD
- Approval decision: Pending
- Approved scope / required changes: Pending
- Approved evaluation targets / required changes: Pending
- Date of written approval: Pending
- Evidence location (email, meeting minutes or signed note): Pending
