from fastapi import APIRouter

from src.api.rbac.routes.index import index_router

rbac_router = APIRouter()
rbac_router.include_router(index_router, tags=["index"])
