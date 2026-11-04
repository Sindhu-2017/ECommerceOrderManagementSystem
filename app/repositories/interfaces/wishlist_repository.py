from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.product import Product
from app.models.wishlist import Wishlist


class WishlistRepositoryInterface(ABC):
    @abstractmethod
    async def get_customer_by_user_id(self,db:AsyncSession,user_id:int)->Customer:
        pass

    @abstractmethod
    async def get_product(self,db:AsyncSession,prouct_id:int)->Product:
        pass

    @abstractmethod
    async def get_existing_wishlist(self,db:AsyncSession,customer_id:int,product_id:int)->Wishlist:
        pass

    @abstractmethod
    async def create(self,db:AsyncSession,wishlist:Wishlist)->Wishlist:
        pass

    @abstractmethod
    async def get_customer_wishlist(seld,db:AsyncSession,customer_id:id)->Wishlist:
        pass

    @abstractmethod
    async def get_by_product_id(self,db:AsyncSession,wishlist_id:int,customer_id:int)->Wishlist|None:
        pass

    @abstractmethod
    async def delete(self,db:AsyncSession,wishlist:Wishlist)->None:
        pass
