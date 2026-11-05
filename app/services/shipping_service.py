import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ShippingInUseError
from app.models.shipping import Shipping
from app.repositories.interfaces.shipping_repository import ShippingRepositoryInterface
from app.schemas.shipping_schema import ShippingCreate, ShippingUpdate

logger = logging.getLogger(__name__)


class ShippingService:
    def __init__(self, shipping_repository: ShippingRepositoryInterface):
        self.shipping_repository = shipping_repository

    async def create_shipping(
        self, db: AsyncSession, user_id: int, data: ShippingCreate
    ) -> Shipping:
        try:
            customer = await self.shipping_repository.get_customer_by_user_id(
                db, user_id
            )

            if customer is None:
                raise ValueError("Customer profile not found")

            existing_addresses = await self.shipping_repository.get_all(
                db, customer.customer_id
            )

            # First address becomes the default address.
            make_default = data.is_default or not existing_addresses

            if make_default:
                for address in existing_addresses:
                    address.is_default = False
            shipping = Shipping(
                customer_id=customer.customer_id,
                recipient_name=data.recipient_name,
                phone=data.phone,
                address_line=data.address_line,
                city=data.city,
                state=data.state,
                pincode=data.pincode,
                is_default=make_default,
            )

            await self.shipping_repository.create(db, shipping)
            await db.commit()
            await db.refresh(shipping)

            logger.info(
                "Shipping address created. shipping_id=%s", shipping.shipping_id
            )
            return shipping

        except Exception:
            await db.rollback()
            logger.exception("Shipping address creation failed")
            raise

    async def get_all_shipping(self, db: AsyncSession, user_id: int) -> list[Shipping]:
        customer = await self.shipping_repository.get_customer_by_user_id(db, user_id)

        if customer is None:
            raise ValueError("Customer profile not found")

        return await self.shipping_repository.get_all(db, customer.customer_id)

    async def get_shipping(
        self, db: AsyncSession, user_id: int, shipping_id: int
    ) -> Shipping:
        customer = await self.shipping_repository.get_customer_by_user_id(db, user_id)

        if customer is None:
            raise ValueError("Customer profile not found")

        shipping = await self.shipping_repository.get_by_id(
            db, shipping_id, customer.customer_id
        )

        if shipping is None:
            raise ValueError("Shipping address not found")

        return shipping

    async def update_shipping(
        self, db: AsyncSession, user_id: int, shipping_id: int, data: ShippingUpdate
    ) -> Shipping:

        try:
            customer = await self.shipping_repository.get_customer_by_user_id(
                db, user_id
            )

            if customer is None:
                raise ValueError("Customer profile not found")

            shipping = await self.shipping_repository.get_by_id(
                db, shipping_id, customer.customer_id
            )

            if shipping is None:
                raise ValueError("Shipping address not found")

            update_data = data.model_dump(exclude_unset=True)

            if update_data.get("is_default") is True:
                addresses = await self.shipping_repository.get_all(
                    db, customer.customer_id
                )

                for address in addresses:
                    address.is_default = False

            for field, value in update_data.items():
                setattr(shipping, field, value)

            await self.shipping_repository.update(db, shipping)
            await db.commit()
            await db.refresh(shipping)

            return shipping

        except Exception:
            await db.rollback()
            logger.exception("Shipping address update failed")
            raise

    async def delete_shipping(
        self, db: AsyncSession, user_id: int, shipping_id: int
    ) -> None:
        try:
            customer = await self.shipping_repository.get_customer_by_user_id(
                db, user_id
            )

            if customer is None:
                raise ValueError("Customer profile not found")

            shipping = await self.shipping_repository.get_by_id(
                db, shipping_id, customer.customer_id
            )

            if shipping is None:
                raise ValueError("Shipping address not found")

            if await self.shipping_repository.has_orders(db, shipping_id):
                raise ShippingInUseError(
                    "Cannot delete this shipping address because it is used in an order"
                )

            await self.shipping_repository.delete(db, shipping)
            await db.commit()

            logger.info("Shipping address deleted. shipping_id=%s", shipping_id)

        except Exception:
            await db.rollback()
            logger.exception("Shipping address deletion failed")
            raise
