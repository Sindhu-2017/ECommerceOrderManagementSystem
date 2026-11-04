import asyncio
import logging
from uuid import uuid4

import razorpay

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.payment import Payment

from app.repositories.interfaces.payment_repository import (
    PaymentRepositoryInterface
)

from app.repositories.interfaces.order_repository import (
    OrderRepositoryInterface
)


logger = logging.getLogger(__name__)
class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepositoryInterface,
        order_repository: OrderRepositoryInterface
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository
        settings = get_settings()

        self.client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET.get_secret_value()
            )
        )

    async def create_payment(self,db: AsyncSession, order_id: int,user_id: int):

        customer = await self.order_repository.get_customer_by_user_id(
            db,user_id
        )
        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        order = await self.payment_repository.get_order(
            db,order_id,customer.customer_id
        )
        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.order_status != "pending":
            raise HTTPException(
                status_code=400,
                detail="Order is not available for payment"
            )

        amount = int(order.total_amount * 100)
        reference_id = f"order_{order_id}_{uuid4().hex[:8]}"

        try:
            payment_link = await asyncio.to_thread(
                self.client.payment_link.create,
                {
                    "amount": amount,
                    "currency": "INR",
                    "accept_partial": False,
                    "description": f"Payment for order {order_id}",
                    "reference_id": reference_id,
                    "customer": {
                        "name": order.shipping_recipient_name,
                        "contact": customer.phone
                    },
                    "notify": {
                        "sms": False,
                        "email": False
                    },
                    "reminder_enable": False
                }
            )

            payment = Payment(
                order_id=order.order_id,
                payment_method="razorpay",
                payment_amount=order.total_amount,
                payment_status="pending",
                razorpay_payment_link_id=payment_link["id"],
                payment_link_url=payment_link["short_url"],
                razorpay_reference_id=reference_id,
            )

            db.add(payment)
            await db.commit()
            await db.refresh(payment)
            logger.info("Payment link created. payment_id=%s",payment.payment_id)

            return {
                "payment_id": payment.payment_id,
                "payment_status": payment.payment_status,
                "payment_link_id": payment_link["id"],
                "payment_url": payment_link["short_url"],
                "amount": amount,
                "currency": "INR"
            }

        except Exception:
            await db.rollback()
            logger.exception("Failed to create payment link")
            raise HTTPException(
                status_code=502,
                detail="Unable to create payment link"
            )

    async def check_payment_status(
        self,
        db: AsyncSession,
        payment_id: int,
        user_id: int
    ):
        customer = await self.order_repository.get_customer_by_user_id(
            db,user_id
        )

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        payment = await db.get(Payment, payment_id)
        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        order = await self.payment_repository.get_order(
            db,payment.order_id,customer.customer_id
        )
        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        # avoid verifying an already successful payment
        if payment.payment_status == "success":
            return {
                "message": "Payment already completed",
                "payment_status": payment.payment_status,
                "order_status": order.order_status,
                "transaction_id": payment.transaction_id
            }

        try:
            # fetch payment link details directly from Razorpay
            payment_link = await asyncio.to_thread(
                self.client.payment_link.fetch,
                payment.razorpay_payment_link_id
            )

            if (
                payment_link.get("reference_id")
                != payment.razorpay_reference_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Razorpay reference ID mismatch"
                )

            if payment_link["status"] != "paid":
                return {
                    "message": "Payment is not completed yet",
                    "payment_status": payment.payment_status,
                    "razorpay_status": payment_link["status"]
                }

            payments = payment_link.get("payments") or []

            captured_payment = next(
                (
                    item for item in payments
                    if item.get("status") == "captured"
                ),
                None
            )

            if captured_payment is None:
                raise HTTPException(
                    status_code=400,
                    detail="Captured payment details not found"
                )
            
            if int(payment_link["amount_paid"]) != int(
                payment.payment_amount * 100
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Payment amount mismatch"
                )

            payment.transaction_id = captured_payment["payment_id"]
            payment.payment_status = "success"

            order.order_status = "paid"

            await db.commit()
            await db.refresh(payment)

            logger.info("Payment verified successfully. payment_id=%s",payment.payment_id)

            return {
                "message": "Payment verified successfully",
                "payment_status": payment.payment_status,
                "order_status": order.order_status,
                "transaction_id": payment.transaction_id
            }

        except HTTPException:
            raise

        except Exception:
            await db.rollback()
            logger.exception("Failed to verify payment")

            raise HTTPException(
                status_code=502,
                detail="Unable to verify payment"
            )
