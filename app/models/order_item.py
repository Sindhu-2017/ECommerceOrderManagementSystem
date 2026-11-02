from decimal import Decimal

from sqlalchemy import Integer,ForeignKey,Numeric
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database.base import Base
# from app.models.product import Product
# from app.models.order import Order

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id :Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.order_id",ondelete="CASCADE"),
        nullable=False
    )

    product_id:Mapped[int] = mapped_column(
        ForeignKey("products.product_id",ondelete="RESTRICT"),
        nullable=False
    )

    quantity:Mapped[int] =mapped_column(
        Integer,
        nullable=False
    )

    unit_price :Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        nullable=False
    )

    subtotal:Mapped[Decimal] =mapped_column(
        Numeric(12,2),
        nullable=False
    )

    order :Mapped["Order"] = relationship(
        back_populates="items"
    )
    product:Mapped["Product"]=relationship(
        back_populates="order_items"
    )