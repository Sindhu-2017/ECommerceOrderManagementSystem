from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_dependencies import get_category_service
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["Categories"])

CategoryServiceDependency = Annotated[CategoryService, Depends(get_category_service)]


# create new category
@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
    summary="Create category",
    description="Creates a new product category.",
)
async def create_category(
    data: CategoryCreate,
    service: CategoryServiceDependency,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.create_category(db, data)


# retrieves all categories
@router.get(
    "/",
    response_model=list[CategoryResponse],
    dependencies=[Depends(require_roles("admin", "customer"))],
    summary="Get all categories",
    description="Retrieves all available categories.",
)
async def get_all_categories(
    service: CategoryServiceDependency, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.get_all_categories(db)


# retrieves category by id
@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    dependencies=[Depends(require_roles("admin", "customer"))],
    summary="Get category by ID",
    description="Retrieves a category using its ID.",
)
async def get_category(
    category_id: int,
    service: CategoryServiceDependency,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.get_category_by_id(db, category_id)


# update category
@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    dependencies=[Depends(require_roles("admin"))],
    summary="Update category",
    description="Updates an existing category.",
)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    service: CategoryServiceDependency,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.update_category(db, category_id, data)


# delete category
@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_roles("admin"))],
    summary="Delete category",
    description="Deletes a category using its ID.",
)
async def delete_category(
    category_id: int,
    service: CategoryServiceDependency,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await service.delete_category(db, category_id)

    return {"message": "Category deleted successfully"}


# retrieves deleted categories
@router.get(
    "/admin/deleted",
    response_model=list[CategoryResponse],
    dependencies=[Depends(require_roles("admin"))],
    summary="Get deleted categories",
    description="Retrieves all deleted categories",
)
async def get_deleted_categories(
    service: CategoryServiceDependency, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.get_deleted_categories(db)


# restore deleted category
@router.patch(
    "/admin/restore/{category_id}",
    dependencies=[Depends(require_roles("admin"))],
    summary="Restore Category",
    description="Restore Deleted Category based on Category ID",
)
async def restore_category(
    category_id: int,
    service: CategoryServiceDependency,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.restore_category(db, category_id)
