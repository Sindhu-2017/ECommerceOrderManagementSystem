from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.order import Order
from app.models.shipping import Shipping
from app.repositories.interfaces.shipping_repository import ShippingRepositoryInterface


class ShippingRepository(ShippingRepositoryInterface):
    async def get_customer_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> Customer | None:

        result = await db.execute(select(Customer).where(Customer.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, shipping: Shipping) -> Shipping:

        db.add(shipping)
        await db.flush()
        return shipping

    async def get_by_id(
        self, db: AsyncSession, shipping_id: int, customer_id: int
    ) -> Shipping | None:

        result = await db.execute(
            select(Shipping).where(
                Shipping.shipping_id == shipping_id, Shipping.customer_id == customer_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, customer_id: int) -> list[Shipping]:

        result = await db.execute(
            select(Shipping)
            .where(Shipping.customer_id == customer_id)
            .order_by(Shipping.is_default.desc(), Shipping.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(self, db: AsyncSession, shipping: Shipping) -> Shipping:
        await db.flush()
        return shipping

    async def delete(self, db: AsyncSession, shipping: Shipping) -> None:

        await db.delete(shipping)
        await db.flush()

    async def has_orders(self, db: AsyncSession, shipping_id: int) -> bool:

        result = await db.execute(
            select(Order.order_id).where(Order.shipping_id == shipping_id).limit(1)
        )

        return result.scalar_one_or_none() is not None
