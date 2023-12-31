import pytest
from httpx import AsyncClient
from core.housify_service import app
from api.router import setup_router


@pytest.fixture
async def client():
    await setup_router(app)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Housify API"}
