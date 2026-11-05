import pytest

@pytest.mark.asyncio
async def test_get_all_products(admin_client):
    response = await admin_client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_product_not_found(admin_client):
    response = await admin_client.get("/api/products/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_all_products_customer(customer_client):
    response= await customer_client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_product_not_found_customer(customer_client):
    response=await customer_client.get("/api/products/999")
    assert response.status_code == 404



@pytest.mark.asyncio
async def test_create_product_invalid_data(admin_client):
    response = await admin_client.post(
        "/api/products/",
        json={
            "category_id": 999,
            "product_name": "",
            "description": "Invalid product",
            "price": -100,
            "stock_quantity": -5,
        },
    )
    assert response.status_code == 422


