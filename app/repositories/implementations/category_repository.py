from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.interfaces.category_repository import CategoryRepositoryInterface


class CategoryRepository(CategoryRepositoryInterface):

    async def get_by_id(
        self,
        db: AsyncSession,
        category_id: int
    ) -> Category | None:
        result = await db.execute(
            select(Category).where(
                Category.category_id == category_id
            )
        )
        return result.scalar_one_or_none()


    async def get_by_name(
        self,
        db: AsyncSession,
        category_name: str
    ) -> Category | None:
        result = await db.execute(
            select(Category).where(
                Category.category_name.ilike(category_name)
            )
        )

        return result.scalar_one_or_none()


    async def get_all(
        self,
        db: AsyncSession
    ) -> list[Category]:

        result = await db.execute(
            select(Category)
            .where(Category.is_active.is_(True))
            .order_by(Category.category_id)
        )
        return list(result.scalars().all())


    async def create(
        self,
        db: AsyncSession,
        category: Category
    ) -> Category:

        db.add(category)
        await db.flush()
        return category


    async def update(
        self,
        db: AsyncSession,
        category: Category
    ) -> Category:

        await db.flush()
        return category
