# Test strategy

Backend unit tests currently live in `backend/tests/`. This directory is reserved for cross-component, integration and end-to-end test plans as modules are added.

Required evaluation suites from the proposal:

- SQL questions with known answers (50–100).
- Router mixed-question set (40+).
- Request extraction set (60+).
- Optimizer formulation evaluation (30 requests, if retained).
- Simulator hand-calculated deterministic fixtures.
- Twin calibration, p5–p95 coverage and policy backtest.
- Security cases for SQL, parameter bounds and template-only optimization.
- User task-time and usability tests with SME managers.

Gold answers and expected values must be human-written or independently verified.
