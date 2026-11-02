from app.core.config import get_settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

settings = get_settings()
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping = True,
    pool_size =5,
    max_overflow =10,
    pool_timeout =30,
    pool_recycle = 1800,
    echo = True
)

SessionLocal =async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)



