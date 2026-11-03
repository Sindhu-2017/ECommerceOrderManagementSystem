import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ShippingInUseError

from app.api.dependencies.auth import require_roles,get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_shipping_service
from app.models.user import User
from app.schemas.shipping_schema import (
    ShippingCreate,
    ShippingUpdate,
    ShippingResponse
)
from app.services.shipping_service import ShippingService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/shipping",
    tags=["Shipping Address Management"]
)

ShippingServiceDependency = Annotated[ShippingService,Depends(get_shipping_service)]

@router.post(
    "/",
    response_model=ShippingResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("customer"))]
)
async def create_shipping(
    data: ShippingCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ShippingServiceDependency,
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.create_shipping(
            db, current_user.user_id, data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get(
    "/",
    response_model=list[ShippingResponse],
    dependencies=[Depends(require_roles("customer"))]

)
async def get_all_shipping(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ShippingServiceDependency,
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.get_all_shipping(
            db, current_user.user_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get(
    "/{shipping_id}",
    response_model=ShippingResponse,
    dependencies=[Depends(require_roles("customer"))]
)
async def get_shipping(
    shipping_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ShippingServiceDependency,
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.get_shipping(
            db, current_user.user_id, shipping_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.patch(
    "/{shipping_id}",
    response_model=ShippingResponse,
    dependencies=[Depends(require_roles("customer"))]
)
async def update_shipping(
    shipping_id: int,
    data: ShippingUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ShippingServiceDependency,
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.update_shipping(
            db,
            current_user.user_id,
            shipping_id,
            data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.delete(
    "/{shipping_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_roles("customer"))]
)
async def delete_shipping(
    shipping_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ShippingServiceDependency,
    current_user: User = Depends(get_current_user)
):
    try:
        await service.delete_shipping(
            db, current_user.user_id, shipping_id
        )

        return {
            "message": "Shipping address deleted successfully"
        }

    except ShippingInUseError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )