from collections.abc import Callable
from typing import Protocol, runtime_checkable

from fastapi import FastAPI

from src.core.application.cors import setup_cors
from src.core.application.routes import include_routers
from src.core.application.exceptions import add_exception_handlers
from src.core.application.staticfiles import mount_staticfiles
from src.core.log import setup_logging


@runtime_checkable
class AppFactory(Protocol):
    def __call__(self) -> FastAPI: ...


class LazyLoadApp:
    def __init__(self, debug: bool, lifespan: Callable) -> None:
        self._app: FastAPI | None = None
        self._debug = debug
        self._lifespan = lifespan

    def _setup_cors(self) -> None:
        setup_cors(self._app)

    def _include_routers(self) -> None:
        include_routers(self._app)

    def _add_exception_handlers(self) -> None:
        add_exception_handlers(self._app)

    def _mount_staticfiles(self) -> None:
        mount_staticfiles(self._app)

    @staticmethod
    def _setup_log() -> None:
        setup_logging()

    def _config_app(self) -> None:
        """app factory for lazy loading"""
        if self._app is None:
            self._app = FastAPI(debug=self._debug, lifespan=self._lifespan)
            self._add_exception_handlers()
            self._include_routers()
            self._setup_cors()
            self._mount_staticfiles()
            self._setup_log()

    @property
    def instance(self) -> FastAPI:
        self._config_app()
        return self._app

    def __call__(self) -> FastAPI:
        return self.instance
