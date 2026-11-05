from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.service_dependencies import get_auth_service
from app.models.user import User
from app.schemas.auth_schema import (
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserProfileResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


# register - it automatically assigns role as customer
@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Creates a new user account.",
)
async def register(
    data: RegisterRequest,
    service: AuthServiceDependency,
    db: AsyncSession = Depends(get_db),
):
    await service.register(db, data)

    return {"message": "Customer registered successfully"}


# login
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticates the user and generates access and refresh tokens.",
)
async def login(
    service: AuthServiceDependency,
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    return await service.login(db, data.username, data.password)


# generates new tokens using existing refresh token
@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh token",
    description="Generates a new access token using a refresh token.",
)
async def refresh(
    data: RefreshRequest,
    service: AuthServiceDependency,
    db: AsyncSession = Depends(get_db),
):
    return await service.refresh_tokens(db, data.refresh_token)


# logout - refresh token will be revoked
@router.post("/logout", response_model=MessageResponse, summary="Logout User")
async def logout(
    data: RefreshRequest,
    service: AuthServiceDependency,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await service.logout(db, data.refresh_token, current_user.user_id)

    return {"message": "Logged out successfully"}


# get current authenticated user info
@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get my profile",
    description="Retrieves the currently authenticated user's profile.",
)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
