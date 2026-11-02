from datetime import datetime,timezone
from jose import JWTError
from fastapi import HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.repositories.interfaces.refresh_token_repository import RefreshTokenRepositoryInterface
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_refresh_token
)

class AuthService:
    def __init__(
        self,
        user_repository:UserRepositoryInterface,
        refresh_token_repository:RefreshTokenRepositoryInterface
    ):
        user_repository = user_repository
        refresh_token_repository=refresh_token_repository


    async def register(self,db:AsyncSession,data):
        try:
            existing_email = await self.user_repository.get_by_email(
                db,data.email
            )
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )


            existing_username = await self.user_repository.get_by_email(
                db,data.username
            )
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="username already registered"
                )

            hashed_password = hash_password(data.password)

            user = await self.user_repository.create_customer_user(
                db=db,
                username=data.username,
                email=data.email,
                hashed_password=hashed_password,
                first_name = data.first_name,
                last_name = data.last_name,
                phone = data.phone,
                date_of_birth = data.date_of_birth
            )

            await db.commit()

            return user

        except Exception:
            await db.rollback()
            raise


    async def login(self,db:AsyncSession,username:str,password:str)->dict:
        user = await self.user_repository.get_by_username(db,username)

        if (
            not user or not verify_password(password,user.hashed_password)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        access_token = create_access_token(
            user.user_id,
            user.role
        )

        refresh_token, expires_at = create_refresh_token(
            user.user_id
        )
        try:
            await self.refresh_token_repository.create(
                db=db,
                user_id=user.user_id,
                token_hash = hash_refresh_token(refresh_token),
                expires_at = expires_at
            )

            await db.commit()

        except Exception:
            await db.rollback()
            raise

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


    async def refresh_token(self,db:AsyncSession,refresh_token:str)->dict:
        try:
            payload = decode_token(refresh_token)

            if payload["type"]  != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        try:
            stored_token = (
                await self.refresh_repository.get_valid_for_update(
                    db,
                    hash_refresh_token(refresh_token)
                )
            )

            if stored_token:
                stored_token.revoked_at = datetime.now(timezone.utc)
                await db.commit()

        except Exception:
            await db.rollback()
            raise

        



            

