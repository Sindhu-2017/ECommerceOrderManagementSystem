from unittest.mock import AsyncMock, Mock

import pytest

from app.services.category_service import CategoryService
from app.core.exceptions import CategoryNotFoundError


@pytest.fixture
def service():
    category_repository = Mock()

    return CategoryService(
        category_repository=category_repository
    )


@pytest.mark.asyncio
async def test_get_category_success(service):
    category = Mock()
    category.category_id = 1
    category.is_active = True

    service.category_repository.get_by_id = AsyncMock(
        return_value=category
    )

    result = await service.get_category_by_id(
        Mock(), 1
    )

    assert result.category_id == 1
    service.category_repository.get_by_id.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_category_not_found(service):
    service.category_repository.get_by_id = AsyncMock(
        return_value=None
    )

    with pytest.raises(CategoryNotFoundError):
        await service.get_category_by_id(Mock(), 999)


@pytest.mark.asyncio
async def test_get_all_categories(service):
    categories = [Mock(), Mock()]

    service.category_repository.get_all = AsyncMock(
        return_value=categories
    )

    result = await service.get_all_categories(Mock())

    assert len(result) == 2