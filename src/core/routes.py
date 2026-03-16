from fastapi import FastAPI

from src.apps.demo.routes import demos_router


def include_routers(app_: FastAPI) -> None:
    """similar to Django urls.py urlpatterns, but better"""
    app_.include_router(router=demos_router, prefix="/demos", tags=["demos"])
