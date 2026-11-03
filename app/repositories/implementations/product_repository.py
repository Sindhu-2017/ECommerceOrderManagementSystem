from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.interfaces.product_repository import (
    ProductRepositoryInterface
)

class ProductRepository(ProductRepositoryInterface):
    async def get_by_id(self,db: AsyncSession, product_id:int)->Product |None:
        result = await db.execute(
            select(Product).where(Product.product_id == product_id)
        )

        return result.scalar_one_or_none()

    async def get_by_name(self,db: AsyncSession, product_name:str) ->Product|None:
        result = await db.execute(
            select(Product).where(Product.product_name == product_name)
        )

        return result.scalar_one_or_none()

    async def get_all(
        self, 
        db: AsyncSession,
        search:str|None =None, 
        category_id:int |None =None, 
        min_price:float |None =None, 
        max_price:float |None =None, 
        skip:int = 0, 
        limit:int = 10
    )->list[Product]:
        query = select(Product).where(
            Product.is_active.is_(True)
        )

        if search is not None:
            query = query.where(
                Product.product_name.ilike(search)
            )

        if category_id is not None:
            query = query.where(
                Product.category_id == category_id
            )

        if min_price is not None:
            query = query.where(
                Product.price >= min_price
            )

        if max_price is not None:
            query = query.where(
                Product.price <= max_price
            )

        query=(query.offset(skip).limit(limit))

        result = await db.execute(query)

        return list(result.scalars().all())

    async def create(self, db: AsyncSession,product:Product)->Product:
        db.add(product)
        await db.flush()
        return Product


    async def update(self, db: AsyncSession,product:Product)->Product:
        await db.flush()
        return Product

        

