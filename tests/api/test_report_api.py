import pytest


@pytest.mark.asyncio
async def test_get_sales_summary(admin_client):
    response = await admin_client.get("/api/reports/sales-summary")
    assert response.status_code == 200
    data = response.json()

    assert "total_orders" in data
    assert "paid_orders" in data
    assert "total_revenue" in data
    assert "pending_orders" in data


@pytest.mark.asyncio
async def test_get_product_sales(admin_client):
    response = await admin_client.get("/api/reports/product-sales")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_customer_cannot_access_sales_report(customer_client):
    response = await customer_client.get("/api/reports/sales-summary")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_customer_cannot_access_products_sales(customer_client):
    response = await customer_client.get("/api/reports/product-sales")
    assert response.status_code == 403
