from fastapi.routing import APIRouter

from src.api.auth.routes.email_verification import email_verification_router
from src.api.auth.routes.login import login_router
from src.api.auth.routes.refresh import refresh_router
from src.api.auth.routes.register import register_router

auth_router = APIRouter()
auth_router.include_router(login_router)
auth_router.include_router(register_router)
auth_router.include_router(refresh_router)
auth_router.include_router(email_verification_router)
