
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.refresh = AsyncMock()
    db.get = AsyncMock()
    return db


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
