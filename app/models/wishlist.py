from datetime import datetime

from sqlalchemy import Integer,DateTime,func,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database.base import Base
# from app.models.customer import Customer
# from app.models.product import Product

class Wishlist(Base):
    __tablename__ = "wishlists"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "product_id",
            name="uq=customer_product_wishlist"
        ),
    )
    wishlist_id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id :Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.customer_id",ondelete="CASCADE"),
        nullable=False
    )

    product_id :Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.product_id",ondelete="CASCADE"),
        nullable=False
    )

    added_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    customer:Mapped["Customer"] = relationship(
        back_populates="wishlists"
    )

    product : Mapped["Product"] = relationship(
        back_populates="wishlist_entries"
    )


