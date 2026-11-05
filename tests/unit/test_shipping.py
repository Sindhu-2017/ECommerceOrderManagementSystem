import pytest

from app.schemas.shipping_schema import ShippingCreate
from app.services.shipping_service import ShippingService


@pytest.mark.asyncio
async def test_create_shipping(mock_db, mock_shipping_repository, sample_customer):
    mock_shipping_repository.get_customer_by_user_id.return_value = sample_customer
    mock_shipping_repository.get_all.return_value = []

    service = ShippingService(mock_shipping_repository)

    data = ShippingCreate(
        recipient_name="Test Customer",
        phone="9876543210",
        address_line="Main Road",
        city="Chennai",
        state="Tamil Nadu",
        pincode="600001",
    )

    result = await service.create_shipping(mock_db, 1, data)

    assert result.customer_id == 1
    assert result.recipient_name == "Test Customer"
    assert result.is_default is True
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_shipping(
    mock_db, mock_shipping_repository, sample_customer, sample_shipping
):
    mock_shipping_repository.get_customer_by_user_id.return_value = sample_customer
    mock_shipping_repository.get_by_id.return_value = sample_shipping

    service = ShippingService(mock_shipping_repository)

    result = await service.get_shipping(mock_db, 1, 1)

    assert result.shipping_id == 1
    assert result.city == "Chennai"
