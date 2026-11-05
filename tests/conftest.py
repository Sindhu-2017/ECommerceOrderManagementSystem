from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.database.base import Base
from app.main import app


# mock database
@pytest.fixture
def mock_db():
    db = MagicMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.refresh = AsyncMock()
    db.get = AsyncMock()
    return db


# sample data
@pytest.fixture
def sample_user():
    return SimpleNamespace(
        user_id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role="customer",
        is_active=True,
    )


@pytest.fixture
def sample_customer():
    return SimpleNamespace(
        customer_id=1,
        user_id=1,
        first_name="Test",
        last_name="Customer",
        phone="9876543210",
    )


@pytest.fixture
def sample_category():
    return SimpleNamespace(
        category_id=1,
        category_name="Electronics",
        description="Electronic products",
        is_active=True,
    )


@pytest.fixture
def sample_product():
    return SimpleNamespace(
        product_id=1,
        category_id=1,
        product_name="Laptop",
        description="Dell Laptop",
        price=Decimal("50000.00"),
        stock_quantity=10,
        image_path=None,
        is_active=True,
    )


@pytest.fixture
def sample_shipping():
    return SimpleNamespace(
        shipping_id=1,
        customer_id=1,
        recipient_name="Test Customer",
        phone="9876543210",
        address_line="Main Road",
        city="Chennai",
        state="Tamil Nadu",
        pincode="600001",
        is_default=True,
        created_at=datetime.now(),
    )


@pytest.fixture
def sample_order():
    return SimpleNamespace(
        order_id=1,
        customer_id=1,
        shipping_id=1,
        total_amount=Decimal("50000.00"),
        order_status="pending",
    )


@pytest.fixture
def sample_payment():
    return SimpleNamespace(
        payment_id=1,
        order_id=1,
        payment_amount=Decimal("50000.00"),
        payment_status="success",
        transaction_id="txn_123",
    )


@pytest.fixture
def sample_wishlist():
    return SimpleNamespace(
        wishlist_id=1,
        customer_id=1,
        product_id=1,
    )


@pytest.fixture
def sample_sales_summary():
    return SimpleNamespace(
        total_orders=10,
        paid_orders=6,
        total_revenue=Decimal("100000.00"),
        pending_orders=4,
    )


# mock repositories
@pytest.fixture
def mock_user_repository():
    repo = MagicMock()
    repo.get_by_username = AsyncMock()
    repo.get_by_email = AsyncMock()
    repo.get_by_phone = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.create_customer_user = AsyncMock()
    repo.get_all_customers = AsyncMock()
    return repo


@pytest.fixture
def mock_refresh_token_repository():
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.get_valid_for_update = AsyncMock()
    return repo


@pytest.fixture
def mock_category_repository():
    repo = MagicMock()
    repo.get_by_name = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.get_deleted_categories = AsyncMock()
    return repo


@pytest.fixture
def mock_product_repository():
    repo = MagicMock()
    repo.get_by_name = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.get_deleted_products = AsyncMock()
    return repo


@pytest.fixture
def mock_shipping_repository():
    repo = MagicMock()
    repo.get_customer_by_user_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.has_orders = AsyncMock()
    return repo


@pytest.fixture
def mock_order_repository():
    repo = MagicMock()
    repo.get_customer_by_user_id = AsyncMock()
    repo.get_shipping = AsyncMock()
    repo.get_product = AsyncMock()
    repo.create_order = AsyncMock()
    repo.get_order_by_id = AsyncMock()
    repo.get_customer_orders = AsyncMock()
    repo.get_all_orders = AsyncMock()
    return repo


@pytest.fixture
def mock_payment_repository():
    repo = MagicMock()
    repo.get_order = AsyncMock()
    return repo


@pytest.fixture
def mock_wishlist_repository():
    repo = MagicMock()
    repo.get_customer_by_user_id = AsyncMock()
    repo.get_product = AsyncMock()
    repo.get_existing_wishlist = AsyncMock()
    repo.get_customer_wishlist = AsyncMock()
    repo.get_by_product_id = AsyncMock()
    repo.create = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_report_repository():
    repo = MagicMock()
    repo.get_sales_summary = AsyncMock()
    repo.get_product_sales = AsyncMock()
    return repo


# integration
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    TestingSessionLocal = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )
    async with TestingSessionLocal() as session:
        yield session


# api
@pytest.fixture
def api_admin():
    return SimpleNamespace(
        user_id=2,
        username="testadmin",
        email="admin@example.com",
        hashed_password="hashed_password",
        role="admin",
        is_active=True,
        created_at=datetime.now(),
        customer=None,
    )


@pytest.fixture
def api_customer():
    return SimpleNamespace(
        user_id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role="customer",
        is_active=True,
        created_at=datetime.now(),
        customer=None,
    )


@pytest_asyncio.fixture
async def admin_client(db_session, api_admin):
    async def override_get_db():
        yield db_session

    async def override_get_current_user():
        return api_admin

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def customer_client(db_session, api_customer):
    async def override_get_db():
        yield db_session

    async def override_get_current_user():
        return api_customer

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def unauthenticated_client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_category_service(sample_category):
    service = MagicMock()

    service.create_category = AsyncMock(return_value=sample_category)
    service.get_all_categories = AsyncMock(return_value=[sample_category])
    service.get_category_by_id = AsyncMock(return_value=sample_category)
    service.update_category = AsyncMock(return_value=sample_category)
    service.delete_category = AsyncMock()
    service.get_deleted_categories = AsyncMock(return_value=[])
    service.restore_category = AsyncMock(
        return_value={"message": "Category restored successfully."}
    )

    return service


@pytest.fixture
def mock_auth_service():
    service = MagicMock()
    service.register = AsyncMock()
    service.login = AsyncMock()
    service.refresh_tokens = AsyncMock()
    service.logout = AsyncMock()
    return service


@pytest.fixture
def mock_product_service(sample_product):
    service = MagicMock()
    service.create_product = AsyncMock(return_value=sample_product)
    service.upload_product_image = AsyncMock(return_value=sample_product)
    service.get_all_products = AsyncMock(return_value=[sample_product])
    service.get_product = AsyncMock(return_value=sample_product)
    service.update_product = AsyncMock(return_value=sample_product)
    service.delete_product = AsyncMock(
        return_value={"message": "Product deleted successfully"}
    )

    service.get_deleted_products = AsyncMock(return_value=[])

    service.restore_product = AsyncMock(
        return_value={"message": "Product restored successfully.."}
    )
    return service


@pytest.fixture
def mock_order_service(sample_order):
    service = MagicMock()
    service.create_order = AsyncMock(return_value=sample_order)
    service.get_order = AsyncMock(return_value=sample_order)
    service.get_customer_orders = AsyncMock(return_value=[sample_order])
    service.get_all_orders = AsyncMock(return_value=[sample_order])
    return service


@pytest.fixture
def mock_shipping_service(sample_shipping):
    service = MagicMock()
    service.create_shipping = AsyncMock(return_value=sample_shipping)
    service.get_all_shipping = AsyncMock(return_value=[sample_shipping])
    service.get_shipping = AsyncMock(return_value=sample_shipping)
    service.update_shipping = AsyncMock(return_value=sample_shipping)
    service.delete_shipping = AsyncMock()
    return service


@pytest.fixture
def mock_payment_service(sample_payment):
    service = MagicMock()
    service.create_payment = AsyncMock(return_value=sample_payment)
    service.check_payment_status = AsyncMock(return_value=sample_payment)
    return service


@pytest.fixture
def mock_wishlist_service(sample_wishlist):
    service = MagicMock()
    service.add_to_wishlist = AsyncMock(return_value=sample_wishlist)
    service.get_wishlist = AsyncMock(return_value=[sample_wishlist])

    service.remove_from_wishlist = AsyncMock(
        return_value={"message": "Product removed from wishlist successfully"}
    )
    return service


@pytest.fixture
def mock_customer_service(sample_customer):
    service = MagicMock()
    service.get_all_customers = AsyncMock(return_value=[sample_customer])
    return service


@pytest.fixture
def mock_report_service(sample_sales_summary):
    service = MagicMock()
    service.get_sales_summary = AsyncMock(return_value=sample_sales_summary)
    service.get_product_sales = AsyncMock(return_value=[])
    return service
