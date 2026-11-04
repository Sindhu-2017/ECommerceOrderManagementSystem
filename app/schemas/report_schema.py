from decimal import Decimal

from pydantic import BaseModel


class SalesSummaryResponse(BaseModel):
    total_orders: int
    paid_orders: int
    total_revenue: Decimal
    pending_orders: int

class ProductSalesResponse(BaseModel):
    product_id: int
    product_name: str
    quantity_sold: int
    total_sales: Decimal