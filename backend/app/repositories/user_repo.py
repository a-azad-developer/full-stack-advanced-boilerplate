import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.api.v1.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """Repository for User model operations."""

    @staticmethod
    async def create(*, session: AsyncSession, user_create: UserCreate) -> User:
        """Create a new user."""
        db_obj = User(
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            full_name=user_create.full_name,
            is_active=user_create.is_active,
            is_superuser=user_create.is_superuser,
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(
        *, session: AsyncSession, db_user: User, user_in: UserUpdate
    ) -> User:
        """Update an existing user."""
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            extra_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        for field, value in {**user_data, **extra_data}.items():
            setattr(db_user, field, value)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def get_by_email(*, session: AsyncSession, email: str) -> User | None:
        """Get a user by email."""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(*, session: AsyncSession, user_id: uuid.UUID) -> User | None:
        """Get a user by ID."""
        return await session.get(User, user_id)

    @staticmethod
    async def authenticate(
        *, session: AsyncSession, email: str, password: str
    ) -> User | None:
        """Authenticate a user with email and password."""
        DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"
        db_user = await UserRepository.get_by_email(session=session, email=email)
        if not db_user:
            verify_password(password, DUMMY_HASH)
            return None
        verified, updated_password_hash = verify_password(
            password, db_user.hashed_password
        )
        if not verified:
            return None
        if updated_password_hash:
            db_user.hashed_password = updated_password_hash
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
        return db_user
