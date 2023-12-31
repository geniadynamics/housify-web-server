import pytest
from httpx import AsyncClient
from core.housify_service import app
from api.router import setup_router
from datetime import date


@pytest.fixture
async def client():
    await setup_router(app)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_create_new_user(client):
    test_user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "hashed_password": "hashed_test_password",
        "gender": 1,
        # "phone": "+1234567890",
        "birth_date": str(date(2000, 1, 1)),
    }
    response = await client.post("/register", json=test_user_data)
    response_data = response.json()

    assert response.status_code == 201
    assert response_data["email"] == test_user_data["email"]
    assert response_data["first_name"] == test_user_data["first_name"]
    assert response_data["last_name"] == test_user_data["last_name"]
    # Note: hashed_password is typically not returned in the response for security reasons
    assert response_data["gender"] == test_user_data["gender"]
    assert response_data["phone"] == test_user_data["phone"]
    assert response_data["birth_date"] == test_user_data["birth_date"]
    # Add assertion for subscription_lvl if it is returned in the response
    # assert response_data['subscription_lvl'] == "Free-Tier" (if included in the response)
