from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.repositories.implementations.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.implementations.user_repository import (
    UserRepository,
)
from app.services.auth_service import AuthService


async def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    return AuthService(
        db=db,
        user_repository=UserRepository(db),
        refresh_token_repository=RefreshTokenRepository(db),
    )