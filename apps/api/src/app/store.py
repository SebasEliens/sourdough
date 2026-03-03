"""Message store abstraction: in-memory (tests/default) or Supabase (when env set)."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Protocol


def _make_entry(id_: str, text: str, timestamp: str) -> dict:
    return {"id": id_, "text": text, "timestamp": timestamp}


class MessageStore(Protocol):
    def list_messages(self) -> list[dict]: ...
    def create_message(self, text: str) -> dict: ...
    def clear_messages(self) -> None: ...


class InMemoryStore:
    def __init__(self) -> None:
        self._messages: list[dict] = []

    def list_messages(self) -> list[dict]:
        return self._messages.copy()

    def create_message(self, text: str) -> dict:
        entry = _make_entry(
            str(uuid.uuid4()),
            text,
            datetime.now(timezone.utc).isoformat(),
        )
        self._messages.insert(0, entry)
        return entry

    def clear_messages(self) -> None:
        self._messages.clear()


_store: MessageStore | None = None


def get_store() -> MessageStore:
    global _store
    if _store is None:
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            from app.store_supabase import SupabaseStore
            _store = SupabaseStore()
        else:
            _store = InMemoryStore()
    return _store
