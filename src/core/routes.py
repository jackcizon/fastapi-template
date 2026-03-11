from fastapi import FastAPI

from src.apps.users.routes import users_router


def include_routers(app_: FastAPI) -> None:
    app_.include_router(router=users_router, prefix="/users", tags=["users"])
