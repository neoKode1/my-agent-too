"""Tests for FastAPI endpoints (root, health, wizard session)."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


# ---------- Root ----------

@pytest.mark.anyio
async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "+12 Monkeys"
    assert "version" in data
    assert data["docs"] == "/docs"


# ---------- Wizard: create session via POST ----------

@pytest.mark.anyio
async def test_wizard_sessions_list(client):
    resp = await client.get("/api/v1/wizard/sessions")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

