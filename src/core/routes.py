from fastapi import FastAPI

from src.apps.auth.routes import auth_router
from src.apps.rbac.routes import rbac_router


def include_routers(app_: FastAPI) -> None:
    """similar to Django urls.py urlpatterns, but better"""
    app_.include_router(router=auth_router, prefix="/auth", tags=["auth"])
    app_.include_router(router=rbac_router, prefix="/rbac", tags=["rbac"])
