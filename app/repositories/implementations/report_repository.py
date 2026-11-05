from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.repositories.interfaces.report_repository import ReportRepositoryInterface
from app.schemas.report_schema import ProductSalesResponse, SalesSummaryResponse


class ReportRepository(ReportRepositoryInterface):
    async def get_sales_summary(self, db: AsyncSession) -> SalesSummaryResponse:
        total_orders = await db.scalar(select(func.count(Order.order_id)))
        paid_orders = await db.scalar(
            select(func.count(Order.order_id)).where(Order.order_status == "paid")
        )
        total_revenue = await db.scalar(
            select(func.sum(Order.total_amount)).where(Order.order_status == "paid")
        )
        pending_orders = await db.scalar(
            select(func.count(Order.order_id)).where(Order.order_status == "pending")
        )
        return SalesSummaryResponse(
            total_orders=total_orders or 0,
            paid_orders=paid_orders or 0,
            total_revenue=total_revenue or Decimal("0.00"),
            pending_orders=pending_orders or 0,
        )

    async def get_product_sales(self, db: AsyncSession) -> list[ProductSalesResponse]:
        result = await db.execute(
            select(
                Product.product_id,
                Product.product_name,
                func.sum(OrderItem.quantity).label("quantity_sold"),
                func.sum(OrderItem.subtotal).label("total_sales"),
            )
            .join(OrderItem, OrderItem.product_id == Product.product_id)
            .join(Order, Order.order_id == OrderItem.order_id)
            .where(Order.order_status == "paid")
            .group_by(Product.product_id, Product.product_name)
            .order_by(func.sum(OrderItem.quantity).desc())
        )

        rows = result.all()
        return [
            ProductSalesResponse(
                product_id=row.product_id,
                product_name=row.product_name,
                quantity_sold=row.quantity_sold,
                total_sales=row.total_sales or Decimal("0.00"),
            )
            for row in rows
        ]
