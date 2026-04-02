from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.auth.schemas.login_schema import LoginRequestSchema, LoginResponseSchema
from src.api.auth.services.login_service import LoginService
from src.core.db.session import get_db

login_router = APIRouter()


@login_router.post("/login/", name="auth:login:post")
async def login(req: LoginRequestSchema, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    resp_dict = await LoginService.login(login_request=req.model_dump(), db=db)
    return JSONResponse(content=LoginResponseSchema(**resp_dict).model_dump())
