import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.v1.deps import CurrentUser, SessionDep
from app.models.task import Item
from app.repositories.task_repo import TaskRepository
from app.api.v1.schemas.task import ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.api.v1.schemas.auth import Message

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
async def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    if current_user.is_superuser:
        items, count = await TaskRepository.get_all(
            session=session, skip=skip, limit=limit
        )
    else:
        items, count = await TaskRepository.get_by_owner(
            session=session, owner_id=current_user.id, skip=skip, limit=limit
        )

    return ItemsPublic(
        data=[ItemPublic.model_validate(item) for item in items], count=count
    )


@router.get("/{id}", response_model=ItemPublic)
async def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    item = await TaskRepository.get_by_id(session=session, item_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item


@router.post("/", response_model=ItemPublic)
async def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    item = await TaskRepository.create(
        session=session, item_in=item_in, owner_id=current_user.id
    )
    return item


@router.put("/{id}", response_model=ItemPublic)
async def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    item = await TaskRepository.get_by_id(session=session, item_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = await TaskRepository.update(
        session=session, db_item=item, item_in=item_in
    )
    return item


@router.delete("/{id}")
async def delete_item(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    item = await TaskRepository.get_by_id(session=session, item_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await TaskRepository.delete(session=session, db_item=item)
    return Message(message="Item deleted successfully")
