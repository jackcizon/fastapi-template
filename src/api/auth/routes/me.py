from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.core.constants import ROLE
from src.core.securities.jwt import jwt_required_dep

me_router = APIRouter()


@me_router.get("/me/", name="auth:me:get", openapi_extra={"role": ROLE.USER.value})
async def me_get(user: User = Depends(jwt_required_dep)) -> JSONResponse:  # pragma: no cover
    """
    personal home page.
    :return:
    """
    return JSONResponse(content={"jwt": "passed", "user_id": user.id})


@me_router.post("/me/{query}", name="auth:me:post", openapi_extra={"role": ROLE.USER.value})
async def me_post(query: str, user: User = Depends(jwt_required_dep)) -> JSONResponse:  # pragma: no cover
    """
    personal home page.
    :return:
    """
    return JSONResponse(content={"jwt": "passed", "user_id": user.id, "query": query})
