from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.services.payment_service import PaymentService

@pytest.mark.asyncio
async def test_payment_rejected_for_paid_order(
    mock_db,
    mock_payment_repository,
    mock_order_repository,
    sample_customer,
    monkeypatch
):
    mock_order_repository.get_customer_by_user_id.return_value = sample_customer
    mock_payment_repository.get_order.return_value = SimpleNamespace(
        order_id=1,
        customer_id=1,
        order_status="paid",
        total_amount=50000,
    )

    fake_settings = SimpleNamespace(
        RAZORPAY_KEY_ID="test_key",
        RAZORPAY_KEY_SECRET=SimpleNamespace(get_secret_value=lambda: "test_secret"),
    )

    monkeypatch.setattr(
        "app.services.payment_service.get_settings",
        lambda: fake_settings,
    )

    fake_client = MagicMock()
    monkeypatch.setattr(
        "app.services.payment_service.razorpay.Client",
        lambda auth: fake_client,
    )

    service = PaymentService(
        mock_payment_repository,
        mock_order_repository,
    )

    with pytest.raises(HTTPException) as exc:
        await service.create_payment(mock_db, 1, 1)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Order is not available for payment"
