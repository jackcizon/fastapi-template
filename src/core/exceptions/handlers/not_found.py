from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse


def not_found_error_handler(request: Request, exc: Any) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})
