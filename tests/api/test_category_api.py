import pytest

from app.api.dependencies.service_dependencies import get_category_service
from app.main import app


@pytest.mark.asyncio
async def test_create_category(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    try:
        response = await admin_client.post(
            "/api/categories/",
            json={"category_name": "Electronics", "description": "Electronic products"},
        )

        assert response.status_code == 201
        assert response.json()["category_name"] == "Electronics"
        mock_category_service.create_category.assert_awaited_once()

    finally:
        app.dependency_overrides.pop(get_category_service, None)


@pytest.mark.asyncio
async def test_create_category_customer(customer_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    try:
        response = await customer_client.post(
            "/api/categories/",
            json={"category_name": "Electronics", "description": "Electronic products"},
        )
        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(get_category_service, None)


@pytest.mark.asyncio
async def test_get_all_categories(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    try:
        response = await admin_client.get("/api/categories/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["category_name"] == "Electronics"

    finally:
        app.dependency_overrides.pop(get_category_service, None)


@pytest.mark.asyncio
async def test_get_all_categories_customer(customer_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    try:
        response = await customer_client.get("/api/categories/")
        assert response.status_code == 200
        assert len(response.json()) == 1
    finally:
        app.dependency_overrides.pop(get_category_service, None)


@pytest.mark.asyncio
async def test_create_category_short_name(admin_client):
    response = await admin_client.post(
        "/api/categories/",
        json={
            "category_name": "A",
            "description": "Invalid category",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_category_by_id(customer_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    response = await customer_client.get("/api/categories/1")
    assert response.status_code == 200
    assert response.json()["category_name"] == "Electronics"


@pytest.mark.asyncio
async def test_get_category_invalid_id(customer_client):
    response = await customer_client.get("/api/categories/abc")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_category(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    response = await admin_client.patch(
        "/api/categories/1",
        json={"category_name": "Updated Electronics"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_customer_cannot_update_category(customer_client):
    response = await customer_client.patch(
        "/api/categories/1",
        json={"category_name": "Updated Electronics"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_category(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    response = await admin_client.delete("/api/categories/1")
    assert response.status_code == 200
    mock_category_service.delete_category.assert_awaited_once()


@pytest.mark.asyncio
async def test_customer_cannot_delete_category(customer_client):
    response = await customer_client.delete("/api/categories/1")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_deleted_categories(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    response = await admin_client.get("/api/categories/admin/deleted")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_customer_cannot_get_deleted_categories(customer_client):
    response = await customer_client.get("/api/categories/admin/deleted")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_restore_category(admin_client, mock_category_service):
    app.dependency_overrides[get_category_service] = lambda: mock_category_service
    response = await admin_client.patch("/api/categories/admin/restore/1")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_customer_cannot_restore_category(customer_client):
    response = await customer_client.patch("/api/categories/admin/restore/1")

    assert response.status_code == 403
