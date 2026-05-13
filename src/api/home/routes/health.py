import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse

health_router = APIRouter()


@health_router.get("/health/", name="health:get")
def health() -> JSONResponse:
    logger = logging.getLogger(__name__)
    logger.info("health check: passed.")
    return JSONResponse(content={"status": "ok"})
