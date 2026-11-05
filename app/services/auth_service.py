import logging
from datetime import UTC, datetime

from jose import JWTError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    DatabaseOperationError,
    DuplicateEmailError,
    DuplicatePhoneError,
    DuplicateUsernameError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    RefreshTokenNotFoundError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.repositories.interfaces.refresh_token_repository import (
    RefreshTokenRepositoryInterface,
)
from app.repositories.interfaces.user_repository import UserRepositoryInterface

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        refresh_token_repository: RefreshTokenRepositoryInterface,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def register(self, db: AsyncSession, data):
        try:
            if await self.user_repository.get_by_email(db, str(data.email)):
                raise DuplicateEmailError("Email already registered.")

            if await self.user_repository.get_by_username(db, data.username):
                raise DuplicateUsernameError("Username already taken.")

            if await self.user_repository.get_by_phone(db, data.phone):
                raise DuplicatePhoneError("Phone number already registered.")

            await self.user_repository.create_customer_user(
                db=db,
                username=data.username,
                email=str(data.email),
                hashed_password=hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                phone=data.phone,
                date_of_birth=data.date_of_birth,
            )

            await db.commit()

            logger.info("Customer registered. username=%s", data.username)

        except (
            DuplicateEmailError,
            DuplicateUsernameError,
            DuplicatePhoneError,
        ):
            await db.rollback()
            raise

        except IntegrityError as exc:
            await db.rollback()
            logger.warning("Registration rejected by database constraint.")
            raise DuplicateEmailError("Registration details already exist.") from exc

        except SQLAlchemyError as exc:
            await db.rollback()
            logger.exception("Database error during registration.")

            raise DatabaseOperationError("Unable to complete registration.") from exc

    async def login(
        self, db: AsyncSession, username: str, password: str
    ) -> dict[str, str]:
        try:
            user = await self.user_repository.get_by_username(db, username)

        except SQLAlchemyError as exc:
            logger.exception("Database error during login.")

            raise DatabaseOperationError("Unable to process login.") from exc

        if user is None or not verify_password(
            password,
            user.hashed_password,
        ):
            logger.warning("Login failed. Invalid credentials. username=%s", username)
            raise InvalidCredentialsError("Invalid username or password.")

        if not user.is_active:
            raise InactiveUserError("User account is inactive.")

        access_token = create_access_token(user.user_id, user.role)

        refresh_token, expires_at = create_refresh_token(user.user_id, user.role)

        try:
            await self.refresh_token_repository.create(
                db=db,
                user_id=user.user_id,
                token_hash=hash_refresh_token(refresh_token),
                expires_at=expires_at,
            )

            await db.commit()

        except SQLAlchemyError as exc:
            await db.rollback()
            logger.exception("Unable to store refresh token.")

            raise DatabaseOperationError("Unable to complete login.") from exc

        logger.info("Login successful. user_id=%s", user.user_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_tokens(
        self, db: AsyncSession, refresh_token: str
    ) -> dict[str, str]:
        try:
            payload = decode_token(refresh_token)

            if payload.get("type") != "refresh":
                raise InvalidTokenError("Refresh token required.")

            user_id = int(payload["sub"])

        except (JWTError, ValueError, KeyError, TypeError) as exc:
            raise InvalidTokenError("Invalid or expired refresh token.") from exc

        try:
            stored_token = await self.refresh_token_repository.get_valid_for_update(
                db, hash_refresh_token(refresh_token)
            )

            if stored_token is None or stored_token.user_id != user_id:
                raise RefreshTokenNotFoundError(
                    "Refresh token is invalid or already used."
                )

            user = await self.user_repository.get_by_id(db, user_id)

            if user is None or not user.is_active:
                raise InactiveUserError("User is inactive.")

            stored_token.revoked_at = datetime.now(UTC)

            new_access_token = create_access_token(
                user.user_id,
                user.role,
            )

            new_refresh_token, expires_at = create_refresh_token(
                user.user_id, user.role
            )

            await self.refresh_token_repository.create(
                db=db,
                user_id=user.user_id,
                token_hash=hash_refresh_token(new_refresh_token),
                expires_at=expires_at,
            )

            await db.commit()

        except (
            RefreshTokenNotFoundError,
            InactiveUserError,
        ):
            await db.rollback()
            raise

        except SQLAlchemyError as exc:
            await db.rollback()

            logger.exception("Refresh token rotation failed.")

            raise DatabaseOperationError("Unable to refresh session.") from exc

        logger.info("Refresh token rotated. user_id=%s", user_id)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    async def logout(
        self, db: AsyncSession, refresh_token: str, current_user_id: int
    ) -> None:
        try:
            payload = decode_token(refresh_token)

            if payload.get("type") != "refresh":
                raise InvalidTokenError("Refresh token required.")

            token_user_id = int(payload["sub"])

        except (JWTError, ValueError, KeyError, TypeError) as exc:
            raise InvalidTokenError("Invalid or expired refresh token.") from exc

        if token_user_id != current_user_id:
            raise InvalidTokenError("Refresh token does not belong to this user.")

        try:
            stored_token = await self.refresh_token_repository.get_valid_for_update(
                db, hash_refresh_token(refresh_token)
            )

            if stored_token is None:
                raise RefreshTokenNotFoundError(
                    "Refresh token is invalid or already revoked."
                )

            stored_token.revoked_at = datetime.now(UTC)
            await db.commit()

        except RefreshTokenNotFoundError:
            await db.rollback()
            raise

        except SQLAlchemyError as exc:
            await db.rollback()

            logger.exception("Logout database operation failed.")

            raise DatabaseOperationError("Unable to log out.") from exc

        logger.info("Logout successful. user_id=%s", current_user_id)
