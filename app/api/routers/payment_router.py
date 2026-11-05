import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user, require_roles
from app.api.dependencies.database import get_db
from app.api.dependencies.service_dependencies import get_payment_service
from app.models.user import User
from app.services.payment_service import PaymentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["Payments"])


# create payment
@router.post(
    "/create/{order_id}",
    dependencies=[Depends(require_roles("customer"))],
    summary="Create payment",
    description="Creates a payment link for an order.",
)
async def create_payment(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service),
):
    try:
        return await payment_service.create_payment(db, order_id, current_user.user_id)

    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to create Razorpay payment")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create payment",
        )


# verify payment
@router.post(
    "/verify/{payment_id}",
    dependencies=[Depends(require_roles("customer"))],
    summary="Verify payment",
    description="Verifies the payment status and updates the order.",
)
async def verify_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service),
):
    return await payment_service.check_payment_status(
        db, payment_id, current_user.user_id
    )
