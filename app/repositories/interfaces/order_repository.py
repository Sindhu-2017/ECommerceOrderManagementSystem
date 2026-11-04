from abc import ABC,abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.models.shipping import Shipping
from app.models.user import User

class OrderRepositoryInterface(ABC):
    @abstractmethod
    async def get_customer_by_user_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> Customer | None:
        pass

    @abstractmethod
    async def get_shipping(
        self,
        db: AsyncSession,
        shipping_id: int,
        customer_id: int
    ) -> Shipping | None:
        pass

    @abstractmethod
    async def get_product(
        self,
        db: AsyncSession,
        product_id: int
    ) -> Product | None:
        pass

    @abstractmethod
    async def create_order(
        self,
        db: AsyncSession,
        order: Order
    ) -> Order:
        pass

    @abstractmethod
    async def get_order_by_id(
        self,
        db: AsyncSession,
        order_id: int,
        customer_id: int | None = None
    ) -> Order | None:
        pass

    @abstractmethod
    async def get_customer_orders(
        self,
        db: AsyncSession,
        customer_id: int
    ) -> list[Order]:
        pass

    async def get_user_by_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> User | None:
        pass

    @abstractmethod
    async def get_all_orders(self,db:AsyncSession)->list[Order]:
        pass