from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.api.auth.schemas.login_schema import LoginRequestSchema
from src.api.auth.services.login_service import LoginService
from src.core.db.session import get_db

login_router = APIRouter()


@login_router.post("/login/", name="auth:login:post")
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> JSONResponse:
    resp = LoginService.login(req=req, db=db)
    return JSONResponse(content={"access": resp.access, "refresh": resp.refresh})
