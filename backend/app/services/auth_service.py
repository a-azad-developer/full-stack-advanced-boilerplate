"""Authentication service for business logic."""
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.models.user import User
from app.services.user_service import UserService


class AuthService:
    """Service for authentication-related business logic."""

    @staticmethod
    async def authenticate_user(
        *, session: AsyncSession, email: str, password: str
    ) -> User | None:
        """Authenticate a user with email and password."""
        return await UserService.authenticate_user(
            session=session, email=email, password=password
        )

    @staticmethod
    def create_access_token(user_id: str) -> str:
        """Create a JWT access token."""
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return security.create_access_token(user_id, expires_delta=expires_delta)
