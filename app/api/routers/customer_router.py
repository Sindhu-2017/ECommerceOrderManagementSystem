from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_customer_service
from app.schemas.customer_schema import CustomerAdminResponse
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/api/admin",
    tags=["Customers"]
)

CustomerServiceDependency = Annotated[CustomerService,Depends(get_customer_service)]

@router.get(
    "/customers",
    response_model=list[CustomerAdminResponse],
    dependencies=[Depends(require_roles("admin"))]
)
async def get_all_customers(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: CustomerServiceDependency
):
    return await service.get_all_customers(db)

