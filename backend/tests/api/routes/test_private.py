from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User


async def test_create_user(client: TestClient, db: AsyncSession) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/private/users/",
        json={
            "email": "pollo@listo.com",
            "password": "password123",
            "full_name": "Pollo Listo",
        },
    )

    assert r.status_code == 200

    data = r.json()

    user = (await db.execute(select(User).where(User.id == data["id"]))).scalar_one_or_none()

    assert user
    assert user.email == "pollo@listo.com"
    assert user.full_name == "Pollo Listo"
