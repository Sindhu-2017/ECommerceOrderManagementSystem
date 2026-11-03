import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    DatabaseOperationError,
)
from app.models.category import Category
from app.repositories.interfaces.category_repository import CategoryRepositoryInterface
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

logger = logging.getLogger(__name__)

class CategoryService:

    def __init__(
        self,
        category_repository: CategoryRepositoryInterface
    ):
        self.category_repository = category_repository


    async def create_category(
        self,
        db: AsyncSession,
        data: CategoryCreate
    ) -> Category:

        try:
            existing_category = (
                await self.category_repository.get_by_name(
                    db,data.category_name
                )
            )

            if existing_category:
                raise CategoryAlreadyExistsError("Category already exists.")

            category = Category(
                category_name=data.category_name,
                description=data.description,
                is_active=True
            )

            created_category = (
                await self.category_repository.create(
                    db,category
                )
            )
            await db.commit()
            await db.refresh(created_category)

            logger.info("Category created. category_id=%s",created_category.category_id)
            return created_category

        except CategoryAlreadyExistsError:
            await db.rollback()
            raise

        except SQLAlchemyError as exc:
            await db.rollback()

            logger.exception("Database error while creating category.")

            raise DatabaseOperationError("Unable to create category.") from exc


    async def get_all_categories(
        self,
        db: AsyncSession
    ) -> list[Category]:

        try:
            return await self.category_repository.get_all(db)

        except SQLAlchemyError as exc:
            logger.exception("Unable to retrieve categories.")

            raise DatabaseOperationError("Unable to retrieve categories.") from exc


    async def get_category_by_id(
        self,
        db: AsyncSession,
        category_id: int
    ) -> Category:

        try:
            category = await self.category_repository.get_by_id(
                db,
                category_id
            )

            if category is None or not category.is_active:
                raise CategoryNotFoundError("Category not found.")

            return category

        except CategoryNotFoundError:
            raise

        except SQLAlchemyError as exc:
            logger.exception("Unable to retrieve category.")

            raise DatabaseOperationError("Unable to retrieve category.") from exc


    async def update_category(
        self,
        db: AsyncSession,
        category_id: int,
        data: CategoryUpdate
    ) -> Category:

        try:
            category = await self.category_repository.get_by_id(
                db,
                category_id
            )

            if category is None or not category.is_active:
                raise CategoryNotFoundError("Category not found.")

            update_data = data.model_dump(exclude_unset=True)

            if not update_data:
                return category

            new_name = update_data.get("category_name")
            if new_name is not None:
                existing_category = (
                    await self.category_repository.get_by_name(
                        db,new_name
                    )
                )

                if (
                    existing_category is not None
                    and existing_category.category_id != category_id
                ):
                    raise CategoryAlreadyExistsError("Category name already exists.")

            for field, value in update_data.items():
                setattr(category, field, value)

            await self.category_repository.update(db, category)

            await db.commit()
            await db.refresh(category)

            logger.info("Category updated. category_id=%s", category_id)

            return category

        except (
            CategoryNotFoundError,
            CategoryAlreadyExistsError
        ):
            await db.rollback()
            raise

        except SQLAlchemyError as exc:
            await db.rollback()

            logger.exception("Database error while updating category.")

            raise DatabaseOperationError("Unable to update category." ) from exc


    async def delete_category(
        self,
        db: AsyncSession,
        category_id: int
    ) -> None:

        try:
            category = await self.category_repository.get_by_id(
                db,category_id
            )

            if category is None or not category.is_active:
                raise CategoryNotFoundError("Category not found.")

            category.is_active = False

            await self.category_repository.update(db, category)

            await db.commit()

            logger.info("Category deactivated. category_id=%s",category_id)

        except CategoryNotFoundError:
            await db.rollback()
            raise

        except SQLAlchemyError as exc:
            await db.rollback()

            logger.exception("Database error while deleting category.")

            raise DatabaseOperationError("Unable to delete category.") from exc