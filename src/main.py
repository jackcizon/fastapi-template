"""entry point for FastAPI APP"""

from fastapi import FastAPI

from src.apps.users.routes import users_router
from src.core.config import app_settings

app = FastAPI(debug=app_settings.debug)

app.include_router(router=users_router, prefix="/users", tags=["users"])
