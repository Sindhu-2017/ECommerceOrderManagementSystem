from abc import ABC,abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_email(self,db,email)->User|None:
        pass

    @abstractmethod
    async def create_customer_user(
        self,
        db:AsyncSession,
        username:str,
        email:str,
        hashed_password:str,
        first_name:str,
        last_name:str,
        phone:str,
        date_of_birth:str
    )->User:
        pass
    
            
    @abstractmethod
    async def get_by_id(self,db:AsyncSession,user_id:int)->User|None:
        pass