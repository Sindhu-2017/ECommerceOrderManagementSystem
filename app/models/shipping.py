from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

# from app.models.customer import Customer
# from app.models.order import Order


class Shipping(Base):
    __tablename__ = "shipping"

    shipping_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False
    )
    recipient_name: Mapped[str] = mapped_column(String(100), nullable=False)

    phone: Mapped[str] = mapped_column(String(10), nullable=False)
    address_line: Mapped[str] = mapped_column(String(200), nullable=False)

    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    pincode: Mapped[str] = mapped_column(String(6), nullable=False)

    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    customer: Mapped["Customer"] = relationship(back_populates="shipping_addresses")

    orders: Mapped[list["Order"]] = relationship(back_populates="shipping_address")
