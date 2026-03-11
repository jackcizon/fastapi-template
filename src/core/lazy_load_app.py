from fastapi import FastAPI

from src.core.cors import setup_cors
from src.core.routes import include_routers


class LazyLoadApp:
    def __init__(self, debug: bool = True):
        self._app: FastAPI | None = None
        self.debug = debug

    def _setup_cors(self):
        setup_cors(self._app)

    def _include_routers(self) -> None:
        include_routers(self._app)

    def _config_app(self) -> None:
        """app factory for lazy loading"""

        self._app = FastAPI(debug=self.debug)
        self._include_routers()
        self._setup_cors()

    @property
    def app(self):
        self._config_app()
        return self._app

    def __call__(self, *args, **kwargs):
        return self.app
