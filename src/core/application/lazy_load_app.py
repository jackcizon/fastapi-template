from fastapi import FastAPI

from src.core.application.cors import setup_cors
from src.core.application.routes import include_routers
from src.core.application.exceptions import add_exception_handlers


class LazyLoadApp:
    def __init__(self, debug: bool = True):
        self._app: FastAPI | None = None
        self.debug = debug

    def _setup_cors(self) -> None:
        setup_cors(self._app)

    def _include_routers(self) -> None:
        include_routers(self._app)

    def _add_exception_handlers(self) -> None:
        add_exception_handlers(self._app)

    def _config_app(self) -> None:
        """app factory for lazy loading"""
        if self._app is None:
            self._app = FastAPI(debug=self.debug)
            self._add_exception_handlers()
            self._include_routers()
            self._setup_cors()

    @property
    def instance(self) -> FastAPI:
        self._config_app()
        return self._app

    def __call__(self) -> FastAPI:
        return self.instance
