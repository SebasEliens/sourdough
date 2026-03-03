from fastapi import Depends, FastAPI
from pydantic import BaseModel, field_validator

from app.store import MessageStore, get_store

app = FastAPI(title="Sourdough API", version="0.1.0")


class CreateMessageBody(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_non_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("text must be non-empty after trim")
        return stripped


@app.get("/")
def root() -> dict:
    """Health/readiness check."""
    return {"ok": True}


@app.get("/messages")
def list_messages(store: MessageStore = Depends(get_store)) -> list:
    """Return all messages (newest first)."""
    return store.list_messages()


@app.post("/messages", status_code=201)
def create_message(
    body: CreateMessageBody,
    store: MessageStore = Depends(get_store),
) -> dict:
    """Create a message and return it."""
    return store.create_message(body.text)
