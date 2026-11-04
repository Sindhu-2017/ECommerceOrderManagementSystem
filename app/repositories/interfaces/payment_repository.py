from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order


class PaymentRepositoryInterface(ABC):

    @abstractmethod
    async def get_order(
        self,
        db: AsyncSession,
        order_id: int,
        customer_id: int
    ) -> Order | None:
        pass

    # @abstractmethod
    # async def create_payment(
    #     self,
    #     db: AsyncSession,
    #     payment: Payment
    # ) -> Payment:
    #     pass

    # @abstractmethod
    # async def get_payment_by_link_id(
    #     self,
    #     db: AsyncSession,
    #     payment_link_id: str
    # ) -> Payment | None:
    #     pass