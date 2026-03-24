"""FastAPI application entrypoint."""

from fastapi import FastAPI

from routes import health, payments

app = FastAPI(title="LUMEN / SOTE API", version="5.1")
app.include_router(health.router)
app.include_router(payments.router)


@app.get("/")
def root() -> dict[str, str]:
    """Simple liveness root endpoint."""
    return {"status": "running"}
