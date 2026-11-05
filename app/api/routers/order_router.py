import logging

from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user, require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_depencies import get_order_service
from app.models.user import User
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# create order
@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("customer"))],
    summary="Create order",
    description="Creates an order with the selected products and shipping address."
)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        return await order_service.create_order(
            db=db,
            user_id=current_user.user_id,
            data=order_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception:
        logger.exception("Failed to create order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create order"
        )


# get order by id
@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles("customer"))],
    summary="Get order by ID",
    description="Retrieves order details using its ID."
)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        return await order_service.get_order(
            db=db,
            order_id=order_id,
            user_id=current_user.user_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except Exception:
        logger.exception("Failed to retrieve order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve order"
        )


# get all orders
@router.get(
    "/",
    response_model=list[OrderResponse],
    dependencies=[Depends(require_roles("customer"))],
    summary="Get customer orders",
    description="Retrieves orders placed by the authenticated customer."
)
async def get_customer_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        return await order_service.get_customer_orders(
            db=db,
            user_id=current_user.user_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except Exception:
        logger.exception("Failed to retrieve customer orders")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve orders"
        )


# get all cutomer's orders
@router.get(
    "/admin/all",
    response_model=list[OrderResponse],
    dependencies=[Depends(require_roles("admin"))],
    summary="Get All Orders",
    description="Get All Customers and Orders(only admin can see)",
)
async def get_all_orders(
    db:AsyncSession=Depends(get_db),
    order_service: OrderService = Depends(get_order_service),
    search:str |None =Query(default=None,description="Search by order id or order status"),
    skip:int = Query(0,ge=0),
    limit:int = Query(10,ge=1,le=100)
):
    return await order_service.get_all_orders(db,search,skip,limit)