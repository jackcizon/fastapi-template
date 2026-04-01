from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.api.auth.schemas.refresh_schema import RefreshRequestSchema
from src.api.auth.services.refresh_service import RefreshService
from src.core.db.session import get_db

refresh_router = APIRouter()


@refresh_router.post("/refresh/", name="auth:refresh:post")
async def refresh(req: RefreshRequestSchema, db: Session = Depends(get_db)) -> JSONResponse:  # pragma: no cover
    resp = RefreshService.refresh(req, db)
    return JSONResponse(content={"access": resp.access})
