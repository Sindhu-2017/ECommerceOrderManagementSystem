import pytest

from app.api.dependencies.service_dependencies import get_shipping_service
from app.core.exceptions import ShippingInUseError
from app.main import app

SHIPPING_RESPONSE = {
    "shipping_id": 1,
    "customer_id": 1,
    "recipient_name": "Test Customer",
    "phone": "9876543210",
    "address_line": "Main Road",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pincode": "600001",
    "is_default": True,
    "created_at": "2026-11-05T10:00:00",
}


@pytest.mark.asyncio
async def test_create_shipping(customer_client, mock_shipping_service):
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.post(
        "/api/shipping/",
        json={
            "recipient_name": "Test Customer",
            "phone": "9876543210",
            "address_line": "Main Road",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600001",
            "is_default": True,
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_shipping_invalid_phone(customer_client):
    response = await customer_client.post(
        "/api/shipping/",
        json={
            "recipient_name": "Test Customer",
            "phone": "12345",
            "address_line": "Main Road",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600001",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_shipping(customer_client, mock_shipping_service):
    mock_shipping_service.get_all_shipping.return_value = [SHIPPING_RESPONSE]
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.get("/api/shipping/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_all_shipping_customer_not_found(
    customer_client, mock_shipping_service
):
    mock_shipping_service.get_all_shipping.side_effect = ValueError(
        "Customer not found"
    )
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.get("/api/shipping/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_shipping_by_id(customer_client, mock_shipping_service):
    mock_shipping_service.get_shipping.return_value = SHIPPING_RESPONSE
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.get("/api/shipping/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_shipping_not_found(customer_client, mock_shipping_service):
    mock_shipping_service.get_shipping.side_effect = ValueError(
        "Shipping address not found"
    )
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.get("/api/shipping/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_shipping(customer_client, mock_shipping_service):
    mock_shipping_service.update_shipping.return_value = SHIPPING_RESPONSE
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.patch(
        "/api/shipping/1",
        json={"city": "Coimbatore"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_shipping_not_found(customer_client, mock_shipping_service):
    mock_shipping_service.update_shipping.side_effect = ValueError(
        "Shipping address not found"
    )
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.patch(
        "/api/shipping/999",
        json={"city": "Coimbatore"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_shipping(customer_client, mock_shipping_service):
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.delete("/api/shipping/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_shipping_in_use(customer_client, mock_shipping_service):
    mock_shipping_service.delete_shipping.side_effect = ShippingInUseError(
        "Shipping address is used by an order"
    )
    app.dependency_overrides[get_shipping_service] = lambda: mock_shipping_service
    response = await customer_client.delete("/api/shipping/1")
    assert response.status_code == 409
