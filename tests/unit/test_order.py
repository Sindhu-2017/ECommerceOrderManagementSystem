
import pytest

from app.services.order_service import OrderService


@pytest.mark.asyncio
async def test_get_customer_orders(
    mock_db,
    mock_order_repository,
    sample_customer,
    sample_order,
):
    mock_order_repository.get_customer_by_user_id.return_value = (
        sample_customer
    )
    mock_order_repository.get_customer_orders.return_value = [sample_order]

    service = OrderService(
        mock_order_repository,
        email_service=None,
    )

    result = await service.get_customer_orders(mock_db, 1)

    assert len(result) == 1
    assert result[0].order_id == 1
    assert result[0].order_status == "pending"


@pytest.mark.asyncio
async def test_get_customer_orders_without_customer(
    mock_db,
    mock_order_repository,
):
    mock_order_repository.get_customer_by_user_id.return_value = None

    service = OrderService(
        mock_order_repository,
        email_service=None,
    )

    with pytest.raises(ValueError):
        await service.get_customer_orders(mock_db, 1)
