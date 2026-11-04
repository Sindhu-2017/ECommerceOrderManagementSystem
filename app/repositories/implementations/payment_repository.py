from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.models.order import Order

from app.repositories.interfaces.payment_repository import (
    PaymentRepositoryInterface
)
class PaymentRepository(PaymentRepositoryInterface):

    async def get_order(
        self,
        db: AsyncSession,
        order_id: int,
        customer_id: int
    ) -> Order | None:

        result = await db.execute(
            select(Order).where(
                Order.order_id == order_id,
                Order.customer_id == customer_id
            )
        )

        return result.scalar_one_or_none()


    # async def create_payment(
    #     self,
    #     db: AsyncSession,
    #     payment: Payment
    # ) -> Payment:

    #     db.add(payment)
    #     await db.flush()
    #     return payment


    # async def get_payment_by_link_id(
    #     self,
    #     db: AsyncSession,
    #     payment_link_id: str
    # ) -> Payment | None:

    #     result = await db.execute(
    #         select(Payment).where(
    #             Payment.razorpay_payment_link_id == payment_link_id
    #         )
    #     )

    #     return result.scalar_one_or_none()