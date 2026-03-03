"""Supabase-backed message store."""

from __future__ import annotations

import os

from supabase import create_client, Client


def _supabase_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


class SupabaseStore:
    def __init__(self) -> None:
        self._client = _supabase_client()

    def list_messages(self) -> list[dict]:
        resp = (
            self._client.table("messages")
            .select("id, text, created_at")
            .order("created_at", desc=True)
            .execute()
        )
        return [
            {
                "id": row["id"],
                "text": row["text"],
                "timestamp": row["created_at"].isoformat()
                if hasattr(row["created_at"], "isoformat")
                else str(row["created_at"]),
            }
            for row in (resp.data or [])
        ]

    def create_message(self, text: str) -> dict:
        resp = (
            self._client.table("messages")
            .insert({"text": text})
            .execute()
        )
        if not resp.data or len(resp.data) == 0:
            raise RuntimeError("Supabase insert returned no row")
        row = resp.data[0]
        return {
            "id": row["id"],
            "text": row["text"],
            "timestamp": row["created_at"].isoformat()
            if hasattr(row["created_at"], "isoformat")
            else str(row["created_at"]),
        }
