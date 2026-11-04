import pytest

from app.services.category_service import CategoryService
from app.schemas.category_schema import CategoryCreate
from app.core.exceptions import (
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
)

@pytest.mark.asyncio
async def test_get_category(
    mock_db,
    mock_category_repository,
    sample_category,
):
    service = CategoryService(mock_category_repository)

    mock_category_repository.get_by_id.return_value = sample_category

    result = await service.get_category_by_id(mock_db, 1)

    assert result.category_id == 1
    assert result.category_name == "Electronics"


@pytest.mark.asyncio
async def test_get_category_not_found(
    mock_db,
    mock_category_repository,
):
    service = CategoryService(mock_category_repository)

    mock_category_repository.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        await service.get_category_by_id(mock_db, 100)


@pytest.mark.asyncio
async def test_create_duplicate_category(
    mock_db,
    mock_category_repository,
    sample_category,
):
    service = CategoryService(mock_category_repository)

    mock_category_repository.get_by_name.return_value = sample_category

    data = CategoryCreate(
        category_name="Electronics",
        description="Electronic products",
    )

    with pytest.raises(CategoryAlreadyExistsError):
        await service.create_category(mock_db, data)

    mock_db.rollback.assert_awaited_once()