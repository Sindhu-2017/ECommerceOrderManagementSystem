from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.customer import Customer
from app.models.user import User
from app.repositories.interfaces.user_repository import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_phone(self, db: AsyncSession, phone: str) -> User | None:
        result = await db.execute(
            select(User).join(Customer).where(Customer.phone == phone)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(
            select(User)
            .options(selectinload(User.customer))
            .where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_customer_user(
        self,
        db: AsyncSession,
        username: str,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        phone: str,
        date_of_birth: str,
    ) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role="customer",
            is_active=True,
        )

        db.add(user)
        await db.flush()

        customer = Customer(
            user_id=user.user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            date_of_birth=date_of_birth,
        )

        db.add(customer)
        await db.flush()
        return user

    async def get_all_customers(
        self, db: AsyncSession, skip: int, limit: int
    ) -> list[Customer]:
        result = await db.execute(
            select(Customer)
            .options(selectinload(Customer.user))
            .order_by(Customer.customer_id)
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())
