from fastapi import FastAPI

app = FastAPI(title="Sourdough API", version="0.1.0")


@app.get("/")
def root() -> dict:
    """Health/readiness check."""
    return {"ok": True}
