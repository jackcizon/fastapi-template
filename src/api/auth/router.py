from fastapi.routing import APIRouter

from src.api.auth.routes.login import login_router
from src.api.auth.routes.me import me_router
from src.api.auth.routes.refresh import refresh_router
from src.api.auth.routes.register import register_router

auth_router = APIRouter()
auth_router.include_router(login_router, tags=["login"])
auth_router.include_router(register_router, tags=["register"])
auth_router.include_router(refresh_router, tags=["refresh"])
auth_router.include_router(me_router, tags=["me"])
