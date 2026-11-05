from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, index=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id", ondelete="RESTRICT"), nullable=False
    )

    shipping_id: Mapped[int] = mapped_column(
        ForeignKey("shipping.shipping_id", ondelete="RESTRICT"), nullable=False
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    order_status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False
    )

    shipping_recipient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    shipping_address_line: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_city: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_state: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_pincode: Mapped[str] = mapped_column(String(10), nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="orders")

    shipping_address: Mapped["Shipping"] = relationship(back_populates="orders")

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
