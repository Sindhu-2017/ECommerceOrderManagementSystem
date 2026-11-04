from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.report_schema import ProductSalesResponse, SalesSummaryResponse


class ReportRepositoryInterface(ABC):
    @abstractmethod
    async def get_sales_summary(self,db: AsyncSession) -> SalesSummaryResponse:
        pass

    @abstractmethod
    async def get_product_sales(self,db: AsyncSession) -> list[ProductSalesResponse]:
        pass