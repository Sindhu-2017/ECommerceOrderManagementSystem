import pytest

from app.api.dependencies.service_dependencies import get_wishlist_service
from app.main import app


@pytest.mark.asyncio
async def test_add_to_wishlist(customer_client, mock_wishlist_service):
    app.dependency_overrides[get_wishlist_service] = lambda: mock_wishlist_service
    response = await customer_client.post("/api/wishlists/1")
    assert response.status_code == 201
    mock_wishlist_service.add_to_wishlist.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_invalid_product_to_wishlist(customer_client):
    response = await customer_client.post("/api/wishlists/abc")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_wishlist(customer_client, mock_wishlist_service):
    mock_wishlist_service.get_wishlist.return_value = []
    app.dependency_overrides[get_wishlist_service] = lambda: mock_wishlist_service
    response = await customer_client.get("/api/wishlists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_admin_cannot_get_wishlist(admin_client):
    response = await admin_client.get("/api/wishlists/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_remove_from_wishlist(customer_client, mock_wishlist_service):
    app.dependency_overrides[get_wishlist_service] = lambda: mock_wishlist_service
    response = await customer_client.delete("/api/wishlists/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_admin_cannot_remove_from_wishlist(admin_client):
    response = await admin_client.delete("/api/wishlists/1")
    assert response.status_code == 403
