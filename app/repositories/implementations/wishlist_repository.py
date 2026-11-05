from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.customer import Customer
from app.models.product import Product
from app.models.wishlist import Wishlist
from app.repositories.interfaces.wishlist_repository import WishlistRepositoryInterface


class WishlistRepository(WishlistRepositoryInterface):
    async def get_customer_by_user_id(self, db: AsyncSession, user_id: int) -> Customer:
        result = await db.execute(select(Customer).where(Customer.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_product(self, db: AsyncSession, prouct_id: int) -> Product:
        result = await db.execute(
            select(Product).where(
                Product.product_id == prouct_id, Product.is_active.is_(True)
            )
        )
        return result.scalar_one_or_none()

    async def get_existing_wishlist(
        self, db: AsyncSession, customer_id: int, product_id: int
    ):
        result = await db.execute(
            select(Wishlist).where(
                Wishlist.customer_id == customer_id, Wishlist.product_id == product_id
            )
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, wishlist: Wishlist) -> Wishlist:
        db.add(wishlist)
        await db.flush()
        return wishlist

    async def get_customer_wishlist(seld, db: AsyncSession, customer_id: int):
        result = await db.execute(
            select(Wishlist)
            .options(selectinload(Wishlist.product))
            .where(Wishlist.customer_id == customer_id)
            .order_by(Wishlist.added_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_product_id(
        self, db: AsyncSession, product_id: int, customer_id: int
    ):
        result = await db.execute(
            select(Wishlist).where(
                Wishlist.product_id == product_id, Wishlist.customer_id == customer_id
            )
        )
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, wishlist: Wishlist) -> None:
        await db.delete(wishlist)
        await db.flush()
