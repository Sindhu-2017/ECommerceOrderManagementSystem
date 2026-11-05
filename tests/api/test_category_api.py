import pytest

from app.api.dependencies.service_depencies import get_category_service
from app.main import app

@pytest.mark.asyncio
async def test_create_category(admin_client,mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    try:
        response = await admin_client.post(
            "/api/categories/",
            json={
                "category_name": "Electronics",
                "description": "Electronic products"
            }
        )

        assert response.status_code == 201
        assert response.json()["category_name"] == "Electronics"
        mock_category_service.create_category.assert_awaited_once()

    finally:
        app.dependency_overrides.pop(get_category_service, None)



@pytest.mark.asyncio
async def test_create_category_customer(customer_client,mock_category_service):
    app.dependency_overrides[get_category_service] = lambda:mock_category_service
    try:
        response = await customer_client.post(
            "/api/categories/",
            json={
                "category_name": "Electronics",
                "description": "Electronic products"
            }
        )
        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(get_category_service,None)


@pytest.mark.asyncio
async def test_get_all_categories(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    try:
        response = await admin_client.get("/api/categories/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["category_name"] == "Electronics"

    finally:
        app.dependency_overrides.pop(get_category_service,  None)

@pytest.mark.asyncio
async def test_get_all_categories_customer(customer_client,mock_category_service):
    app.dependency_overrides[get_category_service]=lambda:mock_category_service
    try:
        response = await customer_client.get("/api/categories/")
        assert response.status_code ==200
        assert len(response.json()) == 1
    finally:
        app.dependency_overrides.pop(get_category_service,None)


