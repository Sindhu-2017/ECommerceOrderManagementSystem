import pytest

from app.api.dependencies.service_dependencies import get_order_service
from app.main import app

ORDER_RESPONSE = {
    "order_id": 1,
    "customer_id": 1,
    "shipping_id": 1,
    "order_date": "2026-11-05T10:00:00",
    "total_amount": 50000,
    "order_status": "pending",
    "shipping_recipient_name": "Test Customer",
    "shipping_phone": "9876543210",
    "shipping_address_line": "Main Road",
    "shipping_city": "Chennai",
    "shipping_state": "Tamil Nadu",
    "shipping_pincode": "600001",
    "items": [],
}


@pytest.mark.asyncio
async def test_create_order(customer_client, mock_order_service):
    mock_order_service.create_order.return_value = ORDER_RESPONSE
    app.dependency_overrides[get_order_service] = lambda: mock_order_service

    response = await customer_client.post(
        "/orders/",
        json={
            "shipping_id": 1,
            "items": [{"product_id": 1, "quantity": 1}],
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_order_without_items(customer_client):
    response = await customer_client.post(
        "/orders/",
        json={"shipping_id": 1, "items": []},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_order(customer_client, mock_order_service):
    mock_order_service.get_order.return_value = ORDER_RESPONSE
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    response = await customer_client.get("/orders/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_order_not_found(customer_client, mock_order_service):
    mock_order_service.get_order.side_effect = ValueError("Order not found")
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    response = await customer_client.get("/orders/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_customer_orders(customer_client, mock_order_service):
    mock_order_service.get_customer_orders.return_value = [ORDER_RESPONSE]
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    response = await customer_client.get("/orders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_admin_cannot_get_customer_orders(admin_client):
    response = await admin_client.get("/orders/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_get_all_orders(admin_client, mock_order_service):
    mock_order_service.get_all_orders.return_value = [ORDER_RESPONSE]
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    response = await admin_client.get("/orders/admin/all")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_customer_cannot_get_all_orders(customer_client):
    response = await customer_client.get("/orders/admin/all")
    assert response.status_code == 403
