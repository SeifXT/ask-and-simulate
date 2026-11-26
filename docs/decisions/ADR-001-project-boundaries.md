# ADR-001: Project boundaries and responsibility split

- **Status:** Accepted by the team as the v3 proposal baseline (supervisor approval pending)
- **Date:** 2026-11-21

## Context

The project combines natural-language analytics, an inventory digital twin and an optimization engine. Without explicit boundaries, the LLM could become responsible for calculations or unsafe actions, and synthetic data could be mistaken for real operational evidence.

## Decision

- The LLM interprets requests, selects tested templates and explains verified outputs.
- Deterministic Python code owns calculations, SQL validation/execution controls, simulation and solver construction.
- SQL access is read-only and restricted in code.
- Every optimizer plan is twin-validated and requires human approval.
- No automatic purchasing or live production integration is in scope.
- WWI is treated as synthetic data; Egyptian EGP costs are sourced inputs or labelled assumptions.
- Core scope is one stock group, 3–5 high-volume products/product groups and one replenishment process.

## Consequences

The architecture favours transparent contracts, deterministic tests, explicit provenance and human approval over autonomous execution. Additional features must not displace core validation and evaluation work.
