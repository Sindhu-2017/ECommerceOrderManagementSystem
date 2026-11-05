import pytest

from app.core.exceptions import CategoryNotFoundError
from app.models.category import Category
from app.repositories.implementations.category_repository import CategoryRepository
from app.services.category_service import CategoryService


@pytest.mark.asyncio
async def test_get_category_by_id(db_session):
    category = Category(
        category_name="Electronics", description="Electronic products", is_active=True
    )

    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    repository = CategoryRepository()
    service = CategoryService(repository)

    result = await service.get_category_by_id(db_session, category.category_id)

    assert result.category_id == category.category_id
    assert result.category_name == "Electronics"
    assert result.is_active is True


@pytest.mark.asyncio
async def test_get_all_categories(db_session):
    db_session.add_all(
        [
            Category(
                category_name="Electronics",
                description="Electronic products",
                is_active=True,
            ),
            Category(
                category_name="Books",
                description="Book products",
                is_active=True,
            ),
        ]
    )

    await db_session.commit()

    repository = CategoryRepository()
    service = CategoryService(repository)

    result = await service.get_all_categories(db_session)

    assert len(result) == 2
    assert result[0].category_name == "Electronics"


@pytest.mark.asyncio
async def test_category_not_found(db_session):
    service = CategoryService(CategoryRepository())

    with pytest.raises(CategoryNotFoundError):
        await service.get_category_by_id(db_session, 999)
