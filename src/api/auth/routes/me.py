from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.core.securities.jwt import jwt_required_dep

me_router = APIRouter()


@me_router.get("/me/", name="auth:me", openapi_extra={"role": "user"})
async def me(user: User = Depends(jwt_required_dep)) -> JSONResponse:  # pragma: no cover
    """
    personal home page.
    :return:
    """
    return JSONResponse(content={"jwt": "passed", "user_id": user.id})
