"""Outside-in tests: HTTP contract only."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_root_returns_ok(client: AsyncClient):
    """GET / returns 200 and ok: true for health check."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


@pytest.mark.asyncio
async def test_get_messages_returns_empty_list_when_no_messages(client: AsyncClient):
    """GET /messages returns 200 and empty list when no messages exist."""
    response = await client.get("/messages")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_messages_creates_and_returns_message(client: AsyncClient):
    """POST /messages with valid text returns 201 and created message with id, text, timestamp."""
    response = await client.post("/messages", json={"text": "hello"})
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert isinstance(body["id"], str)
    assert body["text"] == "hello"
    assert "timestamp" in body
    assert isinstance(body["timestamp"], str)
    # Timestamp should be ISO format
    from datetime import datetime
    datetime.fromisoformat(body["timestamp"].replace("Z", "+00:00"))


@pytest.mark.asyncio
async def test_get_messages_returns_all_entries_newest_first(client: AsyncClient):
    """GET /messages after posting two messages returns both in newest-first order."""
    r1 = await client.post("/messages", json={"text": "first"})
    assert r1.status_code == 201
    r2 = await client.post("/messages", json={"text": "second"})
    assert r2.status_code == 201
    response = await client.get("/messages")
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2
    assert messages[0]["text"] == "second"
    assert messages[1]["text"] == "first"
