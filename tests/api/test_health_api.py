from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies.database import get_db
from app.main import app


@pytest.mark.asyncio
async def test_health_check(unauthenticated_client):
    response = await unauthenticated_client.get("/api/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "connected"


@pytest.mark.asyncio
async def test_health_check_database_error(unauthenticated_client):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=SQLAlchemyError("Database unavailable"))

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    response = await unauthenticated_client.get("/api/health/")
    assert response.status_code == 503
    assert response.json()["detail"]["status"] == "unhealthy"
