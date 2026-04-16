from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.config import settings
from src.core.resources import resources


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    print(f"app:{app} lifespan starting...")
    await resources.init(db_url=settings.database_url, cache_url=settings.cache_url, broker_url=settings.broker_url)
    app.state.resources = resources  # it is just a pointer, no burden.
    yield
    await resources.aclose()
