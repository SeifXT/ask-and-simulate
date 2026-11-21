# Ask & Simulate

**A Natural-Language Analytics Copilot with an Inventory Digital Twin**

A decision-support capstone project with four stages: ask, analyze, simulate, and optimize/recommend. Managers ask questions in plain English; the system routes them to safe read-only Text-to-SQL, a Monte Carlo inventory digital twin, or a template-based LP/MILP optimization engine.

The language model interprets requests, selects tested templates and explains verified outputs. Deterministic code performs calculations and enforces safety controls. A human approves every proposed plan. The application never places orders.

## Project status

Initial engineering scaffold, aligned with the v3 proposal. Modules and contracts will be implemented incrementally against the approved proposal and team task board.

## Scope baseline

- **Dataset:** Microsoft Wide World Importers (WWI), a documented synthetic wholesale/importer dataset, migrated from SQL Server to PostgreSQL.
- **Business layer:** Egyptian costs and constraints in EGP; each input is sourced or explicitly labelled as an assumption.
- **Inventory scope:** one stock group and 3–5 high-volume products (or product groups), one replenishment process.
- **Core paths:** historical SQL analysis, inventory what-if simulation, template-based optimization.
- **Twin parameters:** `demand_multiplier`, `lead_time_multiplier`, `reorder_point`, `order_quantity`, `safety_stock`.
- **Validation:** held-out calibration, p5–p95 interval coverage, policy backtesting.
- **Optimizer:** tested objective/constraint catalog; PuLP + HiGHS; deterministic and scenario-based models; model-card approval; twin validation of every plan.
- **Interface:** FastAPI backend and Next.js web application.
- **Out of scope:** live production integrations, customer personal data, automatic purchasing, multi-warehouse/network optimization, foundation-model fine-tuning, voice/mobile/multilingual support and 3D twin visuals.

See [architecture](docs/architecture.md), [development workflow](docs/development-workflow.md), and [data/assumptions register](docs/data-and-assumptions.md).

## Repository layout

- `backend/`: Python API and domain modules.
- `frontend/`: Next.js application.
- `data/`: data documentation and local-only data locations.
- `docs/`: architecture, decisions, assumptions and team workflow.
- `tests/`: cross-module and integration test guidance.
- `.github/`: continuous-integration workflows and pull-request template.

## Backend quick start

Python 3.11+:

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
uvicorn ask_simulate.main:app --reload
```

The scaffold exposes `GET /health`. Database, model-provider and frontend configuration will be added alongside their implementation tasks.

## Development rules

- Never commit API keys, passwords, private data or local environment files.
- Keep raw datasets under ignored `data/raw/`; commit only approved small fixtures and documentation.
- Enforce read-only SQL in code, not only in prompts.
- Treat stockouts, fill rate and lost sales as simulation-only unless verified observed data supports them.
- Label financial inputs as sourced or assumed; do not present synthetic-data results as real-business evidence.
- Numerical calculations belong in tested Python code. The LLM must not write or execute solver code or alter simulator logic.
- Every answer exposes its SQL, simulation settings or model card, plus definitions and assumptions.
- Every optimizer plan requires human approval and twin validation. No automatic purchasing.
- Use pull requests, peer review and tests; each contributor must be able to explain their own component.

## Planning

The six project roles and work packages are defined in the v3 proposal and mirrored in the [Trello task board](https://trello.com/b/pe8Hx2wR/ask-simulate-project-tasks).

## License

No open-source license has been selected. All rights remain reserved unless a license is added by the project owners.
