from decimal import Decimal

from sqlalchemy import Integer,String,Boolean,ForeignKey,Text,Numeric,CheckConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database.base import Base
# from app.models.category import Category
# from app.models.wishlist import Wishlist
# from app.models.order_item import OrderItem

class Product(Base):
    __tablename__ = "products"

    product_id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    category_id :Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.category_id",ondelete="RESTRICT"),
        nullable=False
    )

    product_name:Mapped[str]= mapped_column(
        String(50),
        index=True,
        unique=True,
        nullable=False
    )

    description:Mapped[str]= mapped_column(
        Text,
        nullable=True
    )

    price :Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        CheckConstraint("price > 0"),
        nullable=False
    )

    stock_quantity:Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("stock_quantity >= 0"),
        default=0,
        nullable=False
    )

    image_path:Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )

    is_active:Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    category :Mapped["Category"] = relationship(
        back_populates="products"
    )

    wishlists :Mapped[list["Wishlist"]] = relationship(
        back_populates="product"
    )

    order_item :Mapped[list["OrderItem"]]=relationship(
        back_populates="product"
    )

