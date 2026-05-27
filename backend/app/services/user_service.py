"""User service for business logic."""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.api.v1.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user-related business logic."""

    @staticmethod
    async def create_user(
        *, session: AsyncSession, user_create: UserCreate
    ) -> User:
        """Create a new user."""
        return await UserRepository.create(session=session, user_create=user_create)

    @staticmethod
    async def get_user_by_email(
        *, session: AsyncSession, email: str
    ) -> User | None:
        """Get a user by email."""
        return await UserRepository.get_by_email(session=session, email=email)

    @staticmethod
    async def get_user_by_id(
        *, session: AsyncSession, user_id: uuid.UUID
    ) -> User | None:
        """Get a user by ID."""
        return await UserRepository.get_by_id(session=session, user_id=user_id)

    @staticmethod
    async def update_user(
        *, session: AsyncSession, db_user: User, user_in: UserUpdate
    ) -> User:
        """Update an existing user."""
        return await UserRepository.update(
            session=session, db_user=db_user, user_in=user_in
        )

    @staticmethod
    async def authenticate_user(
        *, session: AsyncSession, email: str, password: str
    ) -> User | None:
        """Authenticate a user."""
        return await UserRepository.authenticate(
            session=session, email=email, password=password
        )
