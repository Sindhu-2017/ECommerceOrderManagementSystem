from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
router = APIRouter(
    prefix="/api/health",
    tags=["Health"],
)

# checks the database
@router.get(
    "/",
    summary="Check application health",
    description="Checks whether the application and database are available."
)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected"
            }
        ) from exc