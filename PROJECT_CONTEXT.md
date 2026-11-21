# Ask & Simulate — Shared Project Context

**Purpose:** Canonical context for all six team members and their AI workspaces. Read this before proposing changes or generating project code.
**Project:** Ask & Simulate
**Last updated:** 2026-11-21
**Baseline:** Approved v3 proposal and current repository documentation.
**Status:** Initial shared context. Items marked TBD are deliberately unresolved; do not invent values.

## 1. Project in one paragraph

Ask & Simulate is a decision-support capstone: a manager asks a business question in natural language, and the system routes it to historical analysis, inventory what-if simulation, or constrained replenishment optimization. The language model interprets requests and explains verified results. Deterministic application code owns SQL safety, calculations, simulation and solver construction. A human approves every proposed plan. The application never places orders automatically.

## 2. Agreed scope

- **Dataset:** Microsoft Wide World Importers (WWI), a synthetic wholesale/importer sample dataset, migrated from SQL Server to a project-owned PostgreSQL schema.
- **Business layer:** Egyptian costs and constraints in EGP. Every financial input must be identified as sourced or explicitly assumed, with provenance and date.
- **Inventory boundary:** one stock group, 3–5 high-volume products or product groups, and one replenishment process.
- **Core capabilities:** historical SQL analysis, inventory digital-twin simulation, template-based optimization.
- **Twin parameters:** `demand_multiplier`, `lead_time_multiplier`, `reorder_point`, `order_quantity`, `safety_stock`.
- **Validation:** fit/calibrate using the first 70% of history and evaluate on the held-out 30%; report demand error/WAPE, p5–p95 interval coverage, lead-time percentiles and policy backtesting.
- **Optimizer:** tested objective/constraint catalog; Python + PuLP + HiGHS; deterministic and scenario-based models if retained in final scope; model-card approval; twin validation of every proposed plan.
- **Backend/frontend:** FastAPI and Next.js/React.
- **Out of scope:** live production integrations, customer personal data, automatic purchasing, multi-warehouse/network optimization, foundation-model fine-tuning, voice/mobile/multilingual support and 3D twin visuals.

## 3. Four-stage decision loop

1. **ASK / ROUTE:** classify a request as historical SQL, simulation, optimization, clarification or refusal.
2. **ANALYZE:** draft validated read-only SQL, apply semantic definitions, execute under database permissions and resource limits, select a chart, and explain only what returned evidence supports. A code-based checker verifies numeric claims.
3. **SIMULATE:** extract bounded parameters and run Monte Carlo inventory simulation. Return percentile ranges and explicit assumptions.
4. **OPTIMIZE / RECOMMEND:** select tested objective/constraint templates, validate the structured specification, show a model card for manager approval, solve in deterministic code, then test the plan in the twin. Report trade-offs, binding constraints or infeasibility honestly.

## 4. Non-negotiable engineering rules

- SQL must be enforced as read-only in code: single-statement SELECT only, allowlisted tables/columns, row limits and timeouts. A prompt alone is not a security control.
- The LLM must not execute arbitrary Python, write solver code, alter simulator logic or bypass application validation.
- Deterministic, tested code owns calculations, SQL enforcement, simulation and solver construction.
- Validate every input and optimizer catalog selection in code. Clarify or refuse unsupported, unsafe, ambiguous or impossible requests rather than guessing.
- Every recommendation must expose relevant SQL/evidence, simulation settings or model card, definitions and assumptions.
- Every optimizer plan requires human approval and twin validation. No automatic purchasing.
- Distinguish observed data, derived values, model outputs and assumptions in storage, APIs and UI labels.
- Stockouts, fill rate and lost sales are simulation-only unless verified observed data supports them.
- The WWI dataset is synthetic and US-based. An EGP cost layer does not make the operational dataset Egyptian.
- Never commit secrets, credentials, real customer personal data, local .env files or unapproved raw data to GitHub.

## 5. Data and assumptions

Use WWI as the primary dataset. Before implementation depends on it, verify:
- row counts, date coverage, missingness and gaps;
- whether stock history can be reconstructed from transactions (do not assume a current holdings table is historical);
- product sales density for selecting the 3–5 products;
- supplier lead-time availability from order and receipt timestamps;
- delivery timestamps and whether the proposed 70/30 chronological split is viable.

The exact PostgreSQL schema/mappings, chosen stock group/products, opening-stock reconstruction, simulation parameter bounds, objective/constraint catalog, financial values and API contracts are **TBD until their corresponding spike tests/specification/contract tasks are completed**. Do not make up values or present assumptions as verified facts.

For every EGP input record: identifier, value, unit, sourced/assumed classification, source or rationale, date checked and owner. Avoid double-counting lost revenue and lost margin.

## 6. Current technology baseline

- Python 3.11+ for backend/domain logic.
- FastAPI for API.
- PostgreSQL for project database.
- Next.js/React for web application.
- PuLP + HiGHS for optimization.
- Monte Carlo simulation implemented in deterministic, testable Python.
- Specific model provider, ORM, migration tool, charting library, deployment target and exact dependency versions: TBD. Do not add them without a decision and documentation.

## 7. Repository map

- `backend/`: Python API and domain modules.
- `frontend/`: Next.js application.
- `data/`: data documentation and local-only data locations.
- `docs/`: architecture, decisions, assumptions, policies and shared context.
- `tests/`: unit, contract and integration tests.
- `.github/`: CI workflows and pull-request template.
- `README.md`: project overview and quick start.

## 8. Team workflow and AI use

- Follow `docs/development-workflow.md` for branches, pull requests, reviews and definition of done.
- Follow `docs/ai-tool-policy.md` for the team's approved AI-tool use, project-context sharing, agreed risk acceptance and credential handling.
- All six members have acknowledged the AI-tool policy (confirmed by the project lead on 2026-11-21).
- University approval covers the team's use of AI tools. The team has explicitly accepted the risks of sharing project-related sensitive information and active API keys in AI chats/projects and team communication channels.
- Despite that team risk acceptance, credentials must never be committed to GitHub. Use local untracked .env files or approved secret storage. The project lead coordinates rotation of shared keys if exposed.
- No AI usage log is required by the team.
- AI-generated work must be read, understood, tested and independently checked before it is relied on or committed. Contributors must be able to explain their work.

## 9. Source-of-truth documents

When details conflict, raise the conflict rather than silently choosing. Keep these documents aligned:
- `README.md`: approved project overview and scope baseline.
- `docs/architecture.md`: architecture and system invariants.
- `docs/data-and-assumptions.md`: data provenance and financial assumptions.
- `docs/development-workflow.md`: development process and testing expectations.
- `docs/ai-tool-policy.md`: AI use and information-handling policy.
- `PROJECT_CONTEXT.md`: consolidated starting context for team members and AI workspaces; update after each project gate and contract change.
- Trello board: task order, owners, dependencies and acceptance criteria.

## 10. Decisions still required

Do not invent answers to these:
- WWI spike-test results and final stock group/products.
- PostgreSQL schema and table/column mapping.
- Historical stock reconstruction method and opening balance.
- Exact parameter bounds and clamp-versus-reject rules.
- Demand/lead-time distributions and calibration choices.
- Objective and constraint catalog, units, bounds and provenance.
- Final API request/response contracts for `/ask`, `/simulate` and `/optimize`.
- Model provider and any external service choices.
- Final scenario-based optimization scope and sample-average-approximation design.
- Deployment and operational configuration.

## 11. Working instructions for AI assistants

Before suggesting implementation:
1. Read this file and the relevant source-of-truth document(s).
2. Check the current repository code and Trello task acceptance criteria.
3. Preserve the agreed scope and safety invariants.
4. Mark unknowns as TBD and ask before making consequential assumptions.
5. Prefer small, testable changes with explicit file paths and commands.
6. Do not claim code, tests, data, credentials or integrations exist unless verified in the repository or by a successful test.
