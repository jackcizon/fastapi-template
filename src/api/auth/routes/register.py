from fastapi import APIRouter
from starlette.responses import JSONResponse

register_router = APIRouter()


@register_router.post("/register/", name="auth:register:post")  # pragma: no cover
async def register() -> JSONResponse:
    """
    Warning, you should:
     1. give user a role in `Role` table, see ROLE_CHILD_MAP in `src/core/constants.py`
     2. add a record in `User2Role` table when registering success.
    """
    return JSONResponse(content={})
