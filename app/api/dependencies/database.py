from app.database.connection import SessionLocal
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession,None,None] :
    async with SessionLocal()  as db:
        yield db