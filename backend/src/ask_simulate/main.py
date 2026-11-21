"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Ask & Simulate API",
    version="0.1.0",
    description="Natural-language analytics, inventory simulation and decision optimization.",
)


@app.get("/health", tags=["operations"])
async def health() -> dict[str, str]:
    """Return a minimal liveness response."""
    return {"status": "ok"}
