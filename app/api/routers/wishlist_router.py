from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user, require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_wishlist_service
from app.models.user import User
from app.schemas.wishlist_schema import WishlistResponse
from app.services.wishlist_service import WishListService

router =APIRouter(
    prefix="/api/wishlists",
    tags=["Wishlist Management"]
)

WishlistServiceDependency = Annotated[WishListService,Depends(get_wishlist_service)]

# add product to wishlist
@router.post(
    "/{product_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("customer"))],
    summary="Add product",
    description="Adds a product to the customer's wishlist."
)
async def add_to_wishlist(
    product_id:int,
    db:Annotated[AsyncSession,Depends(get_db)],
    current_user:Annotated[User,Depends(get_current_user)],
    ServiceDependency:WishlistServiceDependency
):
    return await ServiceDependency.add_to_wishlist(db,current_user.user_id,product_id)


# retrieves all products from wishlist
@router.get(
    "/",
    response_model=list[WishlistResponse],
    dependencies=[Depends(require_roles("customer"))],
    summary="Get wishlist",
    description="Retrieves all products in the customer's wishlist."
)
async def get_wishlist(
    db:Annotated[AsyncSession,Depends(get_db)],
    current_user:Annotated[User,Depends(get_current_user)],
    ServiceDependency:WishlistServiceDependency
):
    return await ServiceDependency.get_wishlist(db,current_user.user_id)


# delete product from wislist
@router.delete(
    "/{product_id}",
    dependencies=[Depends(require_roles("customer"))],
    summary="Remove product",
    description="Removes a product from the customer's wishlist."
)
async def remove_from_wishlist(
    product_id:int,
    db:Annotated[AsyncSession,Depends(get_db)],
    current_user:Annotated[User,Depends(get_current_user)],
    ServiceDependency:WishlistServiceDependency
):
    return await ServiceDependency.remove_from_wishlist(db,current_user.user_id,product_id)