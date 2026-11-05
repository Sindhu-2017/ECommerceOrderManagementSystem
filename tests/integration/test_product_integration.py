from decimal import Decimal

import pytest

from app.core.exceptions import ProductNotFoundError
from app.models.category import Category
from app.repositories.implementations.category_repository import (
    CategoryRepository,
)
from app.repositories.implementations.product_repository import (
    ProductRepository,
)
from app.schemas.product_schema import ProductCreate
from app.services.product_service import ProductService


@pytest.mark.asyncio
async def test_create_product(db_session):
    category = Category(
        category_name="Electronics", description="Electronic products", is_active=True
    )

    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    service = ProductService(ProductRepository(), CategoryRepository())

    product_data = ProductCreate(
        category_id=category.category_id,
        product_name="Laptop",
        description="Dell Laptop",
        price=Decimal("50000.00"),
        stock_quantity=10,
    )
    result = await service.create_product(db_session, product_data)
    assert result.product_id is not None
    assert result.product_name == "Laptop"
    assert result.price == Decimal("50000.00")
    assert result.stock_quantity == 10


@pytest.mark.asyncio
async def test_get_product(db_session):
    category = Category(
        category_name="Mobiles",
        description="Mobile products",
        is_active=True,
    )

    db_session.add(category)
    await db_session.flush()

    from app.models.product import Product

    product = Product(
        category_id=category.category_id,
        product_name="Smartphone",
        description="Android phone",
        price=Decimal("20000.00"),
        stock_quantity=15,
        is_active=True,
    )

    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    service = ProductService(ProductRepository(), CategoryRepository())

    result = await service.get_product(db_session, product.product_id)

    assert result.product_id == product.product_id
    assert result.product_name == "Smartphone"


@pytest.mark.asyncio
async def test_get_all_products(db_session):
    category = Category(
        category_name="Accessories",
        description="Computer accessories",
        is_active=True,
    )

    db_session.add(category)
    await db_session.flush()

    from app.models.product import Product

    db_session.add(
        Product(
            category_id=category.category_id,
            product_name="Keyboard",
            description="USB keyboard",
            price=Decimal("1500.00"),
            stock_quantity=20,
            is_active=True,
        )
    )

    await db_session.commit()

    service = ProductService(
        ProductRepository(),
        CategoryRepository(),
    )

    result = await service.get_all_products(db_session)

    assert len(result) == 1
    assert result[0].product_name == "Keyboard"


@pytest.mark.asyncio
async def test_product_not_found(db_session):
    service = ProductService(
        ProductRepository(),
        CategoryRepository(),
    )

    with pytest.raises(ProductNotFoundError):
        await service.get_product(db_session, 999)
