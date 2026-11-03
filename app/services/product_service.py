import logging
import uuid

from pathlib import Path

import aiofiles

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

from app.core.exceptions import (
    ProductNotFoundError,
    ProductAlreadyExistsError,
    InvalidProductDataError
)
from app.repositories.interfaces.product_repository import ProductRepositoryInterface
from app.repositories.interfaces.category_repository import CategoryRepositoryInterface


logger = logging.getLogger(__name__)

# Project root/uploads/products
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "products"
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}

class ProductService:
    UPLOAD_DIR = (Path(__file__).resolve().parents[2] / "uploads" / "products")
    ALLOWED_FILE_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }
    MAX_FILE_SIZE = 5 * 1024 * 1024
    CHUNK_SIZE = 1024 * 1024

    def __init__(
        self,
        product_repository:ProductRepositoryInterface,
        category_repository:CategoryRepositoryInterface
    ):
        self.product_repository=product_repository
        self.category_repository = category_repository


    async def create_product(self,db: AsyncSession,data:ProductCreate)->Product:
        category = await self.category_repository.get_by_id(
            db,data.category_id
        )
        if not category or not category.is_active:
            raise InvalidProductDataError("Invalid Category")

        existing = await self.product_repository.get_by_name(
            db,data.product_name
        )

        if existing:
            raise ProductAlreadyExistsError("Product Already exists.")

        product = Product(
            category_id =data.category_id,
            product_name=data.product_name,
            description = data.description,
            price = data.price,
            stock_quantity = data.stock_quantity,
            image_path=None
        )

        try:
            await self.product_repository.create(db,product)
            await db.commit()

            logger.info("Poduct created successfully :%s",product.product_id)
            return product
        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Product creation failed")
            raise



    async def get_all_products(
        self,
        db: AsyncSession,
        search=None,
        category_id=None,
        min_price=None,
        max_price=None,
        skip=0,
        limit=10
    ):
        if (
            min_price is not None and
            max_price is not None and
            min_price > max_price
        ):
            raise InvalidProductDataError("Minimum price cannot exceed maximum price")
        
        return await self.product_repository.get_all(
            db,
            search=search,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit
        )

    # GET PRODUCT BY ID
    async def get_product(self, db: AsyncSession,product_id: int) -> Product:
        product = await self.product_repository.get_by_id(
            db,product_id
        )
        if not product or not product.is_active:
            raise ProductNotFoundError("Product not found")

        return product

    async def update_product(
            self,
            db: AsyncSession,
            product_id:int,
            data:ProductUpdate
    )->Product:
        product = await self.get_product(db,product_id)
        update_data = data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            category = await self.category_repository.get_by_id(
                db,update_data["category_id"]
            )

            if not category or not category.is_active:
                raise InvalidProductDataError("Invalid category")


        if "product_name" in update_data:
            existing = await self.product_repository.get_by_name(
                db,update_data["product_name"]
            )
            if (
                existing and existing.product_id !=product_id
            ):
                raise ProductAlreadyExistsError("Product name already exists")


        for key,value in update_data.items():
            setattr(Product,key,value)

        try:
            await self.product_repository.update(product)
            await db.commit()

            logger.info("Product updated successfully: %s", product_id)

            return product

        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Product update failed")
            raise

    # SOFT DELETE PRODUCT
    async def delete_product(self,db: AsyncSession, product_id: int) -> dict:
        product = await self.get_product(db,product_id)
        product.is_active = False
        try:
            await self.product_repository.update(db,product)
            await db.commit()

            logger.info("Product deactivated: %s", product_id)
            return {"message": "Product deleted successfully"}

        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Product deletion failed")
            raise
    
    async def upload_product_image(self,db:AsyncSession,product_id: int,image: UploadFile) -> Product:
        product = await self.get_product(db,product_id)

        # validate file type
        if image.content_type not in self.ALLOWED_FILE_TYPES:
            raise InvalidProductDataError("Only JPG and PNG images are allowed")

        # Create product upload directory
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        extension = self.ALLOWED_FILE_TYPES[image.content_type]
        unique_filename = f"{uuid.uuid4().hex}{extension}"
        destination = self.UPLOAD_DIR / unique_filename

        total_size = 0

        try:
            async with aiofiles.open(destination, "wb") as output:
                while True:
                    chunk = await image.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    total_size += len(chunk)

                    if total_size > self.MAX_FILE_SIZE:
                        raise InvalidProductDataError("Image size cannot exceed 5 MB")

                    await output.write(chunk)

            # Store relative path in database
            relative_path = destination.relative_to(self.UPLOAD_DIR.parents[1]).as_posix()
            product.image_path = relative_path
            await self.product_repository.update(db,product)
            await db.commit()

            logger.info("Product image uploaded successfully: %s",product_id)
            return product

        except Exception:
            await db.rollback()
            destination.unlink(missing_ok=True)
            logger.exception("Product image upload failed")
            raise

        finally:
            await image.close()
