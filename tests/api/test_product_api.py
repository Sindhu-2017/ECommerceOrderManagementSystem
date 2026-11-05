import pytest

from app.api.dependencies.service_dependencies import get_product_service
from app.main import app


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
    response = await customer_client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_product_not_found_customer(customer_client):
    response = await customer_client.get("/api/products/999")
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


@pytest.mark.asyncio
async def test_create_product(admin_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await admin_client.post(
        "/api/products/",
        json={
            "category_id": 1,
            "product_name": "Laptop",
            "description": "Dell Laptop",
            "price": 50000,
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201
    mock_product_service.create_product.assert_awaited_once()


@pytest.mark.asyncio
async def test_customer_cannot_create_product(customer_client):
    response = await customer_client.post(
        "/api/products/",
        json={
            "category_id": 1,
            "product_name": "Laptop",
            "description": "Dell Laptop",
            "price": 50000,
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_products_with_service(customer_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service

    response = await customer_client.get("/api/products/")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_products_invalid_limit(customer_client):
    response = await customer_client.get("/api/products/?limit=200")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_product_by_id(customer_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await customer_client.get("/api/products/1")
    assert response.status_code == 200
    assert response.json()["product_name"] == "Laptop"


@pytest.mark.asyncio
async def test_get_product_invalid_id(customer_client):
    response = await customer_client.get("/api/products/abc")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_product_image(admin_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await admin_client.post(
        "/api/products/1/image",
        files={"image": ("laptop.jpg", b"test-image", "image/jpeg")},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_image_without_file(admin_client):
    response = await admin_client.post("/api/products/1/image")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_product(admin_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await admin_client.patch(
        "/api/products/1",
        json={"product_name": "Updated Laptop"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_customer_cannot_update_product(customer_client):
    response = await customer_client.patch(
        "/api/products/1",
        json={"product_name": "Updated Laptop"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_product(admin_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await admin_client.delete("/api/products/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_customer_cannot_delete_product(customer_client):
    response = await customer_client.delete("/api/products/1")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_deleted_products(admin_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await admin_client.get("/api/products/admin/deleted")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_customer_cannot_get_deleted_products(customer_client):
    response = await customer_client.get("/api/products/admin/deleted")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_restore_product(admin_client, mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    response = await admin_client.patch("/api/products/admin/restore/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_customer_cannot_restore_product(customer_client):
    response = await customer_client.patch("/api/products/admin/restore/1")
    assert response.status_code == 403
