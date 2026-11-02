from fastapi import FastAPI

from app.core.config import get_settings
from app.api.routers.auth_router import router as auth_router

settings= get_settings()

app = FastAPI(
    title= settings.PROJECT_NAME,
    description="E-Commerce Order Management System API",
    version= "1.0.0"
)
app.include_router(auth_router)

@app.get("/")
async def root() -> dict:
    return {
        "message" : "Welcome to E-Commerce Order Management System API"
    }
