from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_product_service
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

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
    dependencies=[Depends(require_roles("admin"))],
    summary="Create a product",
    description="Creates a new product with its details and image."
)
async def create_product(
    data: ProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ProductServiceDependency
):

    return await service.create_product(db,data)

# UPLOAD PRODUCT IMAGE
@router.post(
    "/{product_id}/image",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_roles("admin"))],
    summary="Upload product image",
    description="Upload Product Image using Product ID"
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

# GET ALL PRODUCTS
@router.get(
    "/",
    response_model=list[ProductResponse],
    dependencies=[Depends(require_roles("admin","customer"))],
    summary="Get all products",
    description="Retrieves all products with filtering and pagination."
)
async def get_all_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ProductServiceDependency,
    search: str | None = Query(default=None,description="Search by Product name"),
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
    dependencies=[Depends(require_roles("admin","customer"))],
    summary="Get product by ID",
    description="Retrieves product details using its ID.",
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
    dependencies=[Depends(require_roles("admin"))],
    summary="Update product by ID",
    description="Update product details using its ID."
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
    dependencies=[Depends(require_roles("admin"))],
    summary="Delete a product",
    description="Deletes a product using its ID."
)
async def delete_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int,
    service: ProductServiceDependency,
):

    return await service.delete_product(db,product_id)


# DELETED PRODUCTS
@router.get(
    "/admin/deleted",
    response_model=list[ProductResponse],
    dependencies=[Depends(require_roles("admin"))],
    summary="Get deleted prodcts",
    description="Retrieves all deleted products"
)
async def get_deleted_products(
    db:Annotated[AsyncSession,Depends(get_db)],
    service:ProductServiceDependency
):
    return await service.get_deleted_products(db)


# restore deleted product
@router.patch(
    "/admin/restore/{product_id}",
    dependencies=[Depends(require_roles("admin"))],
    summary="Restore Product",
    description="Restore Deleted Product based on Product ID"
)
async def restore_product(
    product_id:int,
    db:Annotated[AsyncSession,Depends(get_db)],
    service:ProductServiceDependency
):
    return await service.restore_product(db,product_id)




