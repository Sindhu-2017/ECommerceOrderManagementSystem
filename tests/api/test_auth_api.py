import pytest

from app.api.dependencies.service_dependencies import get_auth_service
from app.main import app


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


@pytest.mark.asyncio
async def test_register_user(customer_client, mock_auth_service):
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    response = await customer_client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
            "phone": "9876543211",
            "date_of_birth": "1995-01-01",
        },
    )

    assert response.status_code == 201
    mock_auth_service.register.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_invalid_data(customer_client):
    response = await customer_client.post(
        "/api/auth/register",
        json={
            "username": "a",
            "email": "invalid",
            "password": "123",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user(customer_client, mock_auth_service):
    mock_auth_service.login.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "token_type": "bearer",
    }

    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    response = await customer_client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_missing_password(customer_client):
    response = await customer_client.post(
        "/api/auth/login",
        data={"username": "testuser"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_refresh_token(customer_client, mock_auth_service):
    mock_auth_service.refresh_tokens.return_value = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
        "token_type": "bearer",
    }
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    response = await customer_client.post(
        "/api/auth/refresh",
        json={"refresh_token": "valid_refresh_token_123456"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_invalid_token(customer_client):
    response = await customer_client.post(
        "/api/auth/refresh",
        json={"refresh_token": "short"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logout_user(customer_client, mock_auth_service):
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    response = await customer_client.post(
        "/api/auth/logout",
        json={"refresh_token": "valid_refresh_token_123456"},
    )
    assert response.status_code == 200
    mock_auth_service.logout.assert_awaited_once()


@pytest.mark.asyncio
async def test_logout_without_login(unauthenticated_client):
    response = await unauthenticated_client.post(
        "/api/auth/logout",
        json={"refresh_token": "valid_refresh_token_123456"},
    )
    assert response.status_code == 401
