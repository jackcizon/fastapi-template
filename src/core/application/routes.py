from fastapi import FastAPI

from src.api.auth.router import auth_router
from src.api.rbac.router import rbac_router
from src.api.user.router import user_router


def include_routers(app_: FastAPI) -> None:
    """similar to Django urls.py urlpatterns, but better"""
    app_.include_router(router=auth_router, prefix="/auth", tags=["auth"])
    app_.include_router(router=rbac_router, prefix="/rbac", tags=["rbac"])
    app_.include_router(router=user_router, prefix="/user", tags=["user"])
