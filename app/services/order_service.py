import logging
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.interfaces.order_repository import OrderRepositoryInterface
from app.schemas.order_schema import OrderCreate
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(
        self, order_repository: OrderRepositoryInterface, email_service: EmailService
    ):
        self.order_repository = order_repository
        self.email_service = email_service

    async def create_order(
        self, db: AsyncSession, user_id: int, data: OrderCreate
    ) -> Order:
        try:
            customer = await self.order_repository.get_customer_by_user_id(db, user_id)

            if customer is None:
                raise ValueError("Customer profile not found")

            shipping = await self.order_repository.get_shipping(
                db, data.shipping_id, customer.customer_id
            )

            if shipping is None:
                raise ValueError("Invalid shipping address")

            total_amount = Decimal("0.00")
            order_items = []

            for item in data.items:
                product = await self.order_repository.get_product(db, item.product_id)

                if product is None:
                    raise ValueError(f"Product {item.product_id} not found")

                if product.stock_quantity < item.quantity:
                    raise ValueError(f"Insufficient stock for {product.product_name}")

                unit_price = product.price
                subtotal = unit_price * item.quantity
                total_amount += subtotal

                order_items.append(
                    OrderItem(
                        product_id=product.product_id,
                        quantity=item.quantity,
                        unit_price=unit_price,
                        subtotal=subtotal,
                    )
                )

            order = Order(
                customer_id=customer.customer_id,
                shipping_id=shipping.shipping_id,
                total_amount=total_amount,
                order_status="pending",
                shipping_recipient_name=shipping.recipient_name,
                shipping_phone=shipping.phone,
                shipping_address_line=shipping.address_line,
                shipping_city=shipping.city,
                shipping_state=shipping.state,
                shipping_pincode=shipping.pincode,
                items=order_items,
            )

            await self.order_repository.create_order(db, order)
            order_id = order.order_id
            await db.commit()
        except Exception:
            await db.rollback()
            logger.exception("Failed to create order")
            raise

        # Email process starts only after successful order creation
        # Email failure must not undo the committed order

        try:
            created_order = await self.order_repository.get_order_by_id(
                db, order.order_id, customer.customer_id
            )

            if created_order is None:
                logger.error(
                    "Order created but could not be retrieved. Order ID: %s", order_id
                )
                raise ValueError("Created order could not be retrieved")

            user = await self.order_repository.get_user_by_id(db, user_id)

            if user:
                email_sent = await self.email_service.send_order_confirmation(
                    receiver=user.email, order=created_order
                )

                if email_sent:
                    logger.info("Order confirmation email sent. Order ID: %s", order_id)
                else:
                    logger.warning(
                        "Order created successfully, but email was not sent. "
                        "Order ID: %s",
                        order_id,
                    )
            else:
                logger.warning(
                    "Order created, but user email was not found. Order ID: %s",
                    order_id,
                )

            return created_order

        except Exception:
            logger.exception(
                "Unexpected error during order confirmation email process. "
                "Order ID: %s",
                order_id,
            )

            # Retrieve and return the committed order even if email fails
            return await self.order_repository.get_order_by_id(
                db, order_id, customer.customer_id
            )

    async def get_order(self, db: AsyncSession, order_id: int, user_id: int) -> Order:
        customer = await self.order_repository.get_customer_by_user_id(db, user_id)

        if customer is None:
            raise ValueError("Customer profile not found")

        order = await self.order_repository.get_order_by_id(
            db, order_id, customer.customer_id
        )

        if order is None:
            raise ValueError("Order not found")

        return order

    async def get_customer_orders(self, db: AsyncSession, user_id: int) -> list[Order]:
        customer = await self.order_repository.get_customer_by_user_id(db, user_id)
        if customer is None:
            raise ValueError("Customer profile not found")

        return await self.order_repository.get_customer_orders(db, customer.customer_id)

    async def get_all_orders(
        self, db: AsyncSession, search: str, skip: int, limit: int
    ) -> list[Order]:
        try:
            return await self.order_repository.get_all_orders(db, search, skip, limit)

        except Exception:
            logger.exception("Failed to retrieve all orders")
            raise
