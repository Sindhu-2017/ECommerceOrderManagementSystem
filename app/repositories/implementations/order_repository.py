from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.shipping import Shipping
from app.models.user import User

from app.repositories.interfaces.order_repository import (
    OrderRepositoryInterface
)

class OrderRepository(OrderRepositoryInterface):

    async def get_customer_by_user_id(self, db: AsyncSession,user_id: int) -> Customer | None:
        result = await db.execute(
            select(Customer).where(
                Customer.user_id == user_id
            )
        )
        return result.scalar_one_or_none()


    async def get_shipping(self,db: AsyncSession,shipping_id: int,customer_id: int) -> Shipping | None:
        result = await db.execute(
            select(Shipping).where(
                Shipping.shipping_id == shipping_id,
                Shipping.customer_id == customer_id
            )
        )

        return result.scalar_one_or_none()


    async def get_product(self,db: AsyncSession,product_id: int) -> Product | None:
        result = await db.execute(
            select(Product).where(
                Product.product_id == product_id,
                Product.is_active.is_(True)
            )
        )
        return result.scalar_one_or_none()


    async def create_order(self,db: AsyncSession,order: Order) -> Order:
        db.add(order)
        await db.flush()
        return order


    async def get_order_by_id(self,db: AsyncSession,order_id: int,customer_id: int | None = None) -> Order | None:
        query = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.order_id == order_id)
        )

        if customer_id is not None:
            query = query.where(Order.customer_id == customer_id)
        result = await db.execute(query)

        return result.scalar_one_or_none()


    async def get_customer_orders(self,db: AsyncSession,customer_id: int) -> list[Order]:
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.customer_id == customer_id)
            .order_by(Order.order_date.desc())
        )
        return list(result.scalars().all())

    async def get_user_by_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> User | None:

        result = await db.execute(
            select(User).where(User.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_all_orders(self, db:AsyncSession)->list[Order]:
        result=await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.order_date.desc())
        )
        return list(result.scalars().all())
