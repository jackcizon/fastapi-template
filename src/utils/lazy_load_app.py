from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.apps.users.routes import users_router
from src.core.config import app_settings
from src.utils.exceptions import BizException


__all__ = ["create_app"]


def _include_routers(app_: FastAPI) -> None:
    app_.include_router(router=users_router, prefix="/users", tags=["users"])


def _register_exceptions_handlers(app_: FastAPI) -> None:
    # 业务异常
    @app_.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message,
            },
        )

    # 参数校验异常
    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "code": 422,
                "message": "parameter validation error",
                "errors": exc.errors(),
            },
        )


def create_app() -> FastAPI:
    """app factory for lazy load"""

    app_ = FastAPI(debug=app_settings.debug)
    _register_exceptions_handlers(app_)
    _include_routers(app_)
    return app_
