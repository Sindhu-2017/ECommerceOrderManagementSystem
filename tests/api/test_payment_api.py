import pytest

from app.api.dependencies.service_dependencies import get_payment_service
from app.main import app


@pytest.mark.asyncio
async def test_create_payment(customer_client, mock_payment_service):
    mock_payment_service.create_payment.return_value = {
        "payment_link_url": "https://example.com/payment",
        "payment_id": 1,
    }

    app.dependency_overrides[get_payment_service] = lambda: mock_payment_service
    response = await customer_client.post("/payments/create/1")
    assert response.status_code == 200
    assert "payment_link_url" in response.json()


@pytest.mark.asyncio
async def test_create_payment_invalid_order(customer_client, mock_payment_service):
    mock_payment_service.create_payment.side_effect = ValueError("Order not found")
    app.dependency_overrides[get_payment_service] = lambda: mock_payment_service
    response = await customer_client.post("/payments/create/999")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_verify_payment(customer_client, mock_payment_service):
    mock_payment_service.check_payment_status.return_value = {
        "payment_status": "success"
    }
    app.dependency_overrides[get_payment_service] = lambda: mock_payment_service
    response = await customer_client.post("/payments/verify/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_admin_cannot_create_payment(admin_client):
    response = await admin_client.post("/payments/create/1")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_verify_payment(admin_client):
    response = await admin_client.post("/payments/verify/1")
    assert response.status_code == 403
