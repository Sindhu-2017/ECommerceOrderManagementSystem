from abc import ABC, abstractmethod
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_email(self,db: AsyncSession,email: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_username(self,db: AsyncSession,username: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_phone(self,db: AsyncSession,phone: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_id(self,db: AsyncSession,user_id: int) -> User | None:
        pass

    @abstractmethod
    async def create_customer_user(
        self,
        db: AsyncSession,
        username: str,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        phone: str,
        date_of_birth: date,
    ) -> User:
        pass

    @abstractmethod
    async def get_all_customers(self, db: AsyncSession,skip:int,limit:int) -> list[Customer]:
        pass
