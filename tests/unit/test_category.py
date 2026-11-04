import pytest

from app.core.exceptions import CategoryAlreadyExistsError
from app.schemas.category_schema import CategoryCreate
from app.services.category_service import CategoryService


@pytest.mark.asyncio
async def test_create_category(mock_db,mock_category_repository):
    mock_category_repository.get_by_name.return_value = None
    mock_category_repository.create.side_effect = (
        lambda db, category: category
    )

    mock_db.refresh.side_effect = lambda category: None

    service = CategoryService(mock_category_repository)

    data = CategoryCreate(
        category_name="Electronics",
        description="Electronic products",
    )

    result = await service.create_category(mock_db, data)

    assert result.category_name == "Electronics"
    assert result.is_active is True
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_duplicate_category(
    mock_db,
    mock_category_repository,
    sample_category,
):
    mock_category_repository.get_by_name.return_value = sample_category

    service = CategoryService(mock_category_repository)

    data = CategoryCreate(
        category_name="Electronics",
        description="Electronic products",
    )

    with pytest.raises(CategoryAlreadyExistsError):
        await service.create_category(mock_db, data)

    mock_db.rollback.assert_awaited_once()
