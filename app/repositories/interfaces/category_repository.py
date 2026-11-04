from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(
        self,
        db: AsyncSession,
        category_id: int
    ) -> Category | None:
        pass

    @abstractmethod
    async def get_by_name(
        self,
        db: AsyncSession,
        category_name: str
    ) -> Category | None:
        pass

    @abstractmethod
    async def get_all(
        self,
        db: AsyncSession
    ) -> list[Category]:
        pass

    @abstractmethod
    async def create(
        self,
        db: AsyncSession,
        category: Category
    ) -> Category:
        pass

    @abstractmethod
    async def update(
        self,
        db: AsyncSession,
        category: Category
    ) -> Category:
        pass

    @abstractmethod
    async def get_deleted_categories(
        self,
        db: AsyncSession
    ) -> list[Category]:
        pass
