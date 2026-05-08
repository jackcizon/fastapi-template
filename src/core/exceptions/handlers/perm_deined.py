from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse


def perm_denied_error_handler(request: Request, exc: Any) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})
