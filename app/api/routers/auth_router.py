from typing import Annotated

from fastapi import APIRouter, Depends, status

# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_auth_service
from app.models.user import User
from app.schemas.auth_schema import (
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    data: RegisterRequest,
    service: AuthServiceDependency,
    db: AsyncSession = Depends(get_db),
):
    await service.register(db, data)

    return {"message": "Customer registered successfully"}


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    service: AuthServiceDependency,
    # data:Annotated[OAuth2PasswordRequestForm,Depends()],
    db: AsyncSession = Depends(get_db),
):
    return await service.login(db, data.username, data.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    service: AuthServiceDependency,
    db: AsyncSession = Depends(get_db),
):
    return await service.refresh_tokens(db, data.refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    data: RefreshRequest,
    service: AuthServiceDependency,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await service.logout(db, data.refresh_token, current_user.user_id)

    return {"message": "Logged out successfully"}
