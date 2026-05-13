from fastapi import APIRouter

from src.api.home.routes.health import health_router
from src.api.home.routes.root import root_router

home_router = APIRouter()
home_router.include_router(root_router)
home_router.include_router(health_router)
