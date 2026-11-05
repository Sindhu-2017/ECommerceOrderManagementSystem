from typing import Annotated

from fastapi import APIRouter, Depends,Query
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


# get all customers
@router.get(
    "/customers",
    response_model=list[CustomerAdminResponse],
    dependencies=[Depends(require_roles("admin"))],
    summary="Get all customers",
    description="Retrieves the registered customer details."
)
async def get_all_customers(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: CustomerServiceDependency,
    skip:int = Query(0,ge=0),
    limit:int = Query(10,ge=1,le=100)
):
    return await service.get_all_customers(db,skip,limit)

