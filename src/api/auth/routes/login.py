from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.api.auth.schemas.login_schema import LoginRequestSchema, LoginResponseSchema
from src.api.auth.services.auth_service import AuthService
from src.core.db.session import get_db

login_router = APIRouter()


@login_router.post("/login/", name="auth:login")
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> JSONResponse:
    service = AuthService()
    access, refresh_ = service.login(req=req, db=db)
    schema = LoginResponseSchema(access=access, refresh=refresh_)
    return JSONResponse(content={"access": schema.access, "refresh": schema.refresh})
