from decimal import Decimal

import pytest

from app.core.exceptions import InvalidProductDataError
from app.schemas.product_schema import ProductCreate
from app.services.product_service import ProductService


@pytest.mark.asyncio
async def test_create_product(
    mock_db,
    mock_product_repository,
    mock_category_repository,
    sample_category,
):
    mock_category_repository.get_by_id.return_value = sample_category
    mock_product_repository.get_by_name.return_value = None

    mock_product_repository.create.side_effect = (
        lambda db, product: setattr(product, "product_id", 1)
    )

    service = ProductService(
        mock_product_repository,
        mock_category_repository,
    )

    data = ProductCreate(
        category_id=1,
        product_name="Laptop",
        description="Dell Laptop",
        price=Decimal("50000.00"),
        stock_quantity=10,
    )

    result = await service.create_product(mock_db, data)

    assert result.product_name == "Laptop"
    assert result.price == Decimal("50000.00")
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_product_invalid_category(
    mock_db,
    mock_product_repository,
    mock_category_repository,
):
    mock_category_repository.get_by_id.return_value = None

    service = ProductService(
        mock_product_repository,
        mock_category_repository,
    )

    data = ProductCreate(
        category_id=99,
        product_name="Laptop",
        price=Decimal("50000.00"),
        stock_quantity=10,
    )

    with pytest.raises(InvalidProductDataError):
        await service.create_product(mock_db, data)
