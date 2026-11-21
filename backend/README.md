# Backend

FastAPI service scaffold. The first endpoint is `GET /health`.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
uvicorn ask_simulate.main:app --reload
```

## Test and lint

```bash
pytest
ruff check .
```

Planned modules will be introduced behind agreed API contracts: routing/request extraction, safe SQL, simulation, optimization, governance and response schemas.
