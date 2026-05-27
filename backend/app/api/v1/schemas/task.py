import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ItemPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None = None
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int
