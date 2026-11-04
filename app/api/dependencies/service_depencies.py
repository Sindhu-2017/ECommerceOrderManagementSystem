from app.repositories.implementations.category_repository import (
    CategoryRepository
)

from app.repositories.implementations.product_repository import (
    ProductRepository
)

from app.repositories.implementations.refresh_token_repository import (
    RefreshTokenRepository
)
from app.repositories.implementations.user_repository import (
    UserRepository
)

from app.repositories.implementations.order_repository import (
    OrderRepository
)
from app.repositories.implementations.shipping_repository import (
    ShippingRepository
)
from app.repositories.implementations.payment_repository import (
    PaymentRepository
)

from app.services.shipping_service import ShippingService

from app.services.order_service import OrderService
from app.services.email_service import EmailService
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService
from app.services.payment_service import PaymentService


def get_auth_service() -> AuthService:
    return AuthService(
        user_repository=UserRepository(),
        refresh_token_repository=RefreshTokenRepository(),
    )



def get_category_service() -> CategoryService:
    return CategoryService(
        category_repository=CategoryRepository()
    )

def get_product_service() -> ProductService:
    return ProductService(
        product_repository=ProductRepository(),
        category_repository=CategoryRepository()
    )

def get_order_service() -> OrderService:
    return OrderService(
        order_repository=OrderRepository(),
        email_service=EmailService()
    )

def get_shipping_service() -> ShippingService:
    return ShippingService(
        shipping_repository=ShippingRepository()
    )

def get_payment_service() -> PaymentService:
    return PaymentService(
        payment_repository=PaymentRepository(),
        order_repository=OrderRepository()
    )