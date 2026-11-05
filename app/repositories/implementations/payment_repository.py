from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.repositories.interfaces.payment_repository import PaymentRepositoryInterface


class PaymentRepository(PaymentRepositoryInterface):
    async def get_order(
        self, db: AsyncSession, order_id: int, customer_id: int
    ) -> Order | None:
        result = await db.execute(
            select(Order).where(
                Order.order_id == order_id, Order.customer_id == customer_id
            )
        )
        return result.scalar_one_or_none()
