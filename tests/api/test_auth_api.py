import pytest

@pytest.mark.asyncio
async def test_get_my_profile(customer_client):
    response = await customer_client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "customer"


@pytest.mark.asyncio
async def test_get_my_profile_without_token(unauthenticated_client):
    response = await unauthenticated_client.get("/api/auth/me")
    assert response.status_code == 401
