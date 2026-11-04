import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.core.logging_config
from app.api.routers.auth_router import router as auth_router
from app.api.routers.category_router import router as category_router
from app.api.routers.product_router import router as product_router
from app.api.routers.order_router import router as order_router 
from app.api.routers.shipping_router import router as shipping_router
from app.api.routers.payment_router import router as payment_router
from app.api.routers.wishlist_router import router as wishlist_router


from app.core.exceptions import (
    AppError,
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    DatabaseOperationError,
    DuplicateEmailError,
    DuplicatePhoneError,
    DuplicateUsernameError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    RefreshTokenNotFoundError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    InvalidProductDataError,
    OrderNotFoundError,
    InvalidOrderOperationError,
    CustomerNotFoundError
)
from app.middleware.observability import ObservabilityMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-Commerce Order Management System",
    description="E-Commerce API",
    version="1.0.0",
)


@app.exception_handler(AppError)
async def app_exception_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:

    status_codes = {
        InvalidCredentialsError: 401,
        InactiveUserError: 403,
        DuplicateEmailError: 409,
        DuplicateUsernameError: 409,
        DuplicatePhoneError: 409,
        InvalidTokenError: 401,
        RefreshTokenNotFoundError: 401,
        DatabaseOperationError: 500,
        CategoryNotFoundError:404,
        CategoryAlreadyExistsError:409,
        ProductNotFoundError:404,
        ProductAlreadyExistsError:409,
        InvalidProductDataError:400 ,
        CustomerNotFoundError:404,
        OrderNotFoundError:404,
        InvalidOrderOperationError:409       
    }

    status_code = status_codes.get(type(exc), 400)

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(shipping_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(wishlist_router)
app.add_middleware(ObservabilityMiddleware)


@app.get("/")
async def home() -> dict[str, str]:
    return {
        "message": "E-Commerce Order Management System API is running"
    }
