from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.core.config import settings
from src.core.resources import resources


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    print(f"app:{app} lifespan starting...")
    await resources.init(
        db_url=settings.database_url,
        cache_url=settings.cache_url,
        broker_url=settings.broker_url,
        s3_region=settings.s3_region,
        s3_access_key_id=settings.s3_access_key_id,
        s3_access_key_secret=settings.s3_access_key_secret,
        doc_db_url=settings.doc_db_url,
    )
    yield
    await resources.aclose()
