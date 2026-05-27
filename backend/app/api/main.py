from fastapi import APIRouter

from app.api.v1.routes import auth, private, tasks, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(tasks.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
