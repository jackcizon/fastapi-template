from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.core.config import STATIC_DIR


def mount_staticfiles(app_: FastAPI) -> None:
    app_.mount(path="/static", app=StaticFiles(directory=STATIC_DIR))
