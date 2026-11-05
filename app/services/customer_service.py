import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseOperationError
from app.models.customer import Customer
from app.repositories.interfaces.user_repository import UserRepositoryInterface

logger = logging.getLogger(__name__)
class CustomerService:
    def __init__(self,user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def get_all_customers(self,db: AsyncSession,skip:int,limit:int) -> list[Customer]:
        try:
            return await self.user_repository.get_all_customers(db,skip,limit)
        except SQLAlchemyError:
            logger.exception("Unable to retrieve customers.")
            raise DatabaseOperationError("Unable to retrieve customers.")