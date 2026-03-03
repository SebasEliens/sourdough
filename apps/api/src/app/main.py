import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sourdough API", version="0.1.0")

# In-memory store (newest first)
_messages: list[dict] = []


class CreateMessageBody(BaseModel):
    text: str


@app.get("/")
def root() -> dict:
    """Health/readiness check."""
    return {"ok": True}


@app.get("/messages")
def list_messages() -> list:
    """Return all messages (newest first)."""
    return _messages.copy()


@app.post("/messages", status_code=201)
def create_message(body: CreateMessageBody) -> dict:
    """Create a message and return it."""
    entry = {
        "id": str(uuid.uuid4()),
        "text": body.text.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _messages.insert(0, entry)
    return entry
