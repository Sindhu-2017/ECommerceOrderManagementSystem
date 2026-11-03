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

from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService

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