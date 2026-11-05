import pytest


@pytest.mark.asyncio
async def test_admin_get_customers(admin_client):
    response = await admin_client.get("/api/admin/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_customer_cannot_get_customers(customer_client):
    response = await customer_client.get("/api/admin/customers")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_customer_list_invalid_limit(admin_client):
    response = await admin_client.get("/api/admin/customers?limit=200")
    assert response.status_code == 422
