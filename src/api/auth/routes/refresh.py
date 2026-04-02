from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.auth.schemas.refresh_schema import RefreshRequestSchema, RefreshResponseSchema
from src.api.auth.services.refresh_service import RefreshService
from src.core.db.session import get_db

refresh_router = APIRouter()


@refresh_router.post("/refresh/", name="auth:refresh:post")
async def refresh(req: RefreshRequestSchema, db: AsyncSession = Depends(get_db)) -> JSONResponse:  # pragma: no cover
    resp_dict = await RefreshService.refresh(req.model_dump(), db)
    return JSONResponse(content=RefreshResponseSchema(**resp_dict).model_dump())
