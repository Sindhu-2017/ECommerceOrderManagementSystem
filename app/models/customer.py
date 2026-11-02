from datetime import date

from sqlalchemy import Integer,String,Date,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database.base import Base
# from app.models.user import User
# from app.models.wishlist import Wishlist
# from app.models.order import Order
# from app.models.shipping import Shipping

class Customer(Base):
    __tablename__ = "customers"

    customer_id :Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id :Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id",ondelete ="CASCADE"),
        unique=True,
        nullable=False
    )

    first_name :Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_name :Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    phone :Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    date_of_birth :Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    user:Mapped["User"] = relationship(
        back_populates="customer"
    )

    wishlists :Mapped[list["Wishlist"]] = relationship(
        back_populates= "customer",
        cascade= "all,delete-orphan"
    )

    shipping_addresses :Mapped[list["Shipping"]] = relationship(
        back_populates="customer",
        cascade="all,delete-orphan"
    )
    orders :Mapped[list["Order"]] = relationship(
        back_populates="customer"
    )