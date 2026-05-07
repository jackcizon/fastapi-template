from typing import Any

from starlette.responses import JSONResponse
from starlette.requests import Request


def bad_request_error_handler(request: Request, exc: Any) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})
