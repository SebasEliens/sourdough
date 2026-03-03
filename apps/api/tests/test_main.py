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
