from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order


class PaymentRepositoryInterface(ABC):
    @abstractmethod
    async def get_order(
        self, db: AsyncSession, order_id: int, customer_id: int
    ) -> Order | None:
        pass
