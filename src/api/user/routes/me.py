from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.api.user.schemas.me_schema import MeResponseSchema
from src.api.user.services.me_service import MeService
from src.core.db.session import get_db
from src.core.securities.jwt import jwt_required_dep

me_router = APIRouter()


@me_router.get("/me/", name="user:me:get")
async def me(user: User = Depends(jwt_required_dep), db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    personal home page.
    :return:
    """
    resp_dict = await MeService.home_page(user.id, db)
    return JSONResponse(content=MeResponseSchema(**resp_dict).model_dump())
