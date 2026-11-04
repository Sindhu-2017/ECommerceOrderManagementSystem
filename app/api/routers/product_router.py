from fastapi import (
    APIRouter,
    Depends,
    Query,
    UploadFile,
    File,
    status
)

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.services.product_service import ProductService

from app.api.dependencies.service_depencies import (
    get_product_service
)

from app.api.dependencies.auth import require_roles


router = APIRouter(
    prefix="/api/products",
    tags=["Product Management"]
)

ProductServiceDependency = Annotated[ProductService,Depends(get_product_service)]

# CREATE PRODUCT
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))]
)
async def create_product(
    data: ProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ProductServiceDependency
):

    return await service.create_product(db,data)


# GET ALL PRODUCTS
@router.get(
    "/",
    response_model=list[ProductResponse],
    dependencies=[Depends(require_roles("admin","customer"))]
)
async def get_all_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ProductServiceDependency,
    search: str | None = None,
    category_id: int | None = Query(default=None, gt=0),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):

    return await service.get_all_products(
        db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit
    )


# GET PRODUCT BY ID
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(require_roles("admin","customer"))]
)
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int,
    service: ProductServiceDependency
):

    return await service.get_product(db,product_id)


# UPDATE PRODUCT
@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(require_roles("admin"))]
)
async def update_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int,
    data: ProductUpdate,
    service:ProductServiceDependency
):

    return await service.update_product(db,product_id, data)


# DELETE PRODUCT
@router.delete(
    "/{product_id}",
    dependencies=[Depends(require_roles("admin"))]
)
async def delete_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int,
    service: ProductServiceDependency,
):

    return await service.delete_product(db,product_id)

# @router.get(
#         "/admin/deleted",
#         response_model=list[ProductResponse],
#         dependencies=[Depends(require_roles("admin"))]
# )
# async def get_deleted_products(
#     db
# )

# UPLOAD PRODUCT IMAGE
@router.post(
    "/{product_id}/image",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_roles("admin"))]
)
async def upload_product_image(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int,
    service: ProductServiceDependency,
    image: UploadFile = File(...),
):

    return await service.upload_product_image(
        db,product_id,
        image
    )

