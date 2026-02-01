"""entry point for FastAPI APP"""

from fastapi import FastAPI

from src.apps.users.routes import users_router
from src.core.config import settings

app = FastAPI(debug=settings.debug)

app.include_router(router=users_router, prefix="/users", tags=["users"])
