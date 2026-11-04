import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from app.models.wishlist import Wishlist

from app.repositories.interfaces.wishlist_repository import WishlistRepositoryInterface

logger= logging.getLogger(__name__)

class WishListService():
    def __init__(self,wishlist_repository:WishlistRepositoryInterface):
        self.wishlist_repository = wishlist_repository

    async def add_to_wishlist(self,db:AsyncSession,user_id:int,product_id:int):
        customer =await self.wishlist_repository.get_customer_by_user_id(db,user_id)
        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        product =await self.wishlist_repository.get_product(db,product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        existing_wishlist =await self.wishlist_repository.get_existing_wishlist(
            db,customer.customer_id,product_id
        )

        if existing_wishlist is not None:
            raise HTTPException(
                status_code=409,
                detail="Product already exists in wishlist"
            )

        wishlist =Wishlist(
            customer_id=customer.customer_id,
            product_id=product_id
        )
        try:
            await self.wishlist_repository.create(db,wishlist)
            await db.commit()
            await db.refresh(wishlist)

            logger.info("Product added to wishlist. wishlist_id=%s", wishlist.wishlist_id)
            return wishlist

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Product already exists in wishlist"
            )
        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Failed to add product to wishlist")
            raise HTTPException(
                status_code=500,
                detail="Unable to add product in wishlist"
            )

    async def get_wishlist(self,db:AsyncSession,user_id:int):
        customer =await self.wishlist_repository.get_customer_by_user_id(db,user_id)
        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return await self.wishlist_repository.get_customer_wishlist(db,customer.customer_id)

    async def remove_from_wishlist(self,db:AsyncSession,user_id:int,product_id:int):
        customer =await self.wishlist_repository.get_customer_by_user_id(db,user_id)
        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        wishlist =await self.wishlist_repository.get_by_product_id(db,product_id,customer.customer_id)

        if wishlist is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found in wishlist"
            )

        try:
            await self.wishlist_repository.delete(db,wishlist)
            await db.commit()
            logger.info("Product removed from wishlist. product_id=%s", product_id)

            return {
                "message": "Product removed from wishlist successfully"
            }

        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Failed to remove product from wishlist")
            raise HTTPException(
                status_code=500,
                detail="Unable to remove product from wishlist"
            )



        


    






