from decimal import Decimal
from datetime import datetime

from sqlalchemy import String,DateTime,ForeignKey,Numeric,func
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database.base import Base
# from app.models.order import Order

class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String(30), 
        nullable=False
    )

    payment_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    payment_status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    order: Mapped["Order"] = relationship(
        back_populates="payments"
    )