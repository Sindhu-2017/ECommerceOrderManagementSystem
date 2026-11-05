import pytest

from app.services.auth_service import AuthService
from app.api.routers.auth_router import get_my_profile
from app.core.exceptions import InvalidCredentialsError

@pytest.mark.asyncio
async def test_login_invalid_credentials(
    mock_db,
    mock_user_repository,
    mock_refresh_token_repository,
    monkeypatch,
):
    mock_user_repository.get_by_username.return_value = None
    monkeypatch.setattr(
        "app.services.auth_service.verify_password",
        lambda password, hashed: False,             
    )
    service = AuthService(
        mock_user_repository,
        mock_refresh_token_repository,
    )
    with pytest.raises(InvalidCredentialsError):
        await service.login(mock_db, "wronguser", "wrongpassword")


@pytest.mark.asyncio
async def test_get_my_profile(sample_user):
    result = await get_my_profile(current_user=sample_user)
    assert result.user_id == 1
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.role == "customer"
