import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseOperationError
from app.repositories.interfaces.report_repository import ReportRepositoryInterface
from app.schemas.report_schema import ProductSalesResponse, SalesSummaryResponse

logger = logging.getLogger(__name__)
class ReportService:
    def __init__(self,report_repository: ReportRepositoryInterface):
        self.report_repository = report_repository

    async def get_sales_summary(self,db: AsyncSession) -> SalesSummaryResponse:
        try:
            return await self.report_repository.get_sales_summary(db)
        except SQLAlchemyError as exc:
            logger.exception("Failed to generate sales summary report")
            raise DatabaseOperationError(
                "Unable to generate sales summary report"
            ) from exc

    async def get_product_sales(self,db: AsyncSession) -> list[ProductSalesResponse]:
        try:
            return await self.report_repository.get_product_sales(db)

        except SQLAlchemyError as exc:
            logger.exception("Failed to generate product sales report")
            raise DatabaseOperationError(
                "Unable to generate product sales report"
            ) from exc