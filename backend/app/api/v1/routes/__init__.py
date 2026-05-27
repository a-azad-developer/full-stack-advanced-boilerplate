"""Routes package."""
from app.api.v1.routes import users, auth, tasks, utils, private

__all__ = ["users", "auth", "tasks", "utils", "private"]
