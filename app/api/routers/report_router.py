from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_report_service
from app.schemas.report_schema import ProductSalesResponse, SalesSummaryResponse
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)

ReportServiceDependency = Annotated[ReportService,Depends(get_report_service)]


# retrieve sales summary report
@router.get(
    "/sales-summary",
    response_model=SalesSummaryResponse,
    dependencies=[Depends(require_roles("admin"))],
    summary="Sales summary",
    description="Retrieves the overall sales summary."
)
async def get_sales_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ReportServiceDependency
):
    return await service.get_sales_summary(db)


# retrieve product sales report
@router.get(
    "/product-sales",
    response_model=list[ProductSalesResponse],
    dependencies=[Depends(require_roles("admin"))],
    summary="Product sales",
    description="Retrieves sales information for individual products."
)
async def get_product_sales(
    db: Annotated[AsyncSession, Depends(get_db)],
    service: ReportServiceDependency
):
    return await service.get_product_sales(db)