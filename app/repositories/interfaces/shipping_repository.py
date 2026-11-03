from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.shipping import Shipping


class ShippingRepositoryInterface(ABC):

    @abstractmethod
    async def get_customer_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> Customer | None:
        pass

    @abstractmethod
    async def create(
        self, db: AsyncSession, shipping: Shipping
    ) -> Shipping:
        pass

    @abstractmethod
    async def get_by_id(
        self, db: AsyncSession, shipping_id: int, customer_id: int
    ) -> Shipping | None:
        pass

    @abstractmethod
    async def get_all(
        self, db: AsyncSession, customer_id: int
    ) -> list[Shipping]:
        pass

    @abstractmethod
    async def update(
        self, db: AsyncSession, shipping: Shipping
    ) -> Shipping:
        pass

    @abstractmethod
    async def delete(
        self, db: AsyncSession, shipping: Shipping
    ) -> None:
        pass

    @abstractmethod
    async def has_orders(
        self,
        db: AsyncSession,
        shipping_id: int
    ) -> bool:
        pass