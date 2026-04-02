import os
import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import Settings
from src.core.db.models import Base
from src.core.db.session import get_db
from src.main import app

test_settings = Settings("test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", test_settings.database_url)  # ci docker test db
if TEST_DATABASE_URL.startswith("postgresql://"):
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif TEST_DATABASE_URL.startswith("postgresql+psycopg2://"):
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        poolclass=NullPool,  # must use it
    )
    return engine


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_db(test_engine):
    async with test_engine.connect() as conn:
        trans = await conn.begin()

        session_factory = async_sessionmaker(
            bind=conn,  # bind conn, not engine, otherwise may cause `different loop error`
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

        await trans.rollback()


@pytest.fixture
async def test_client(test_db):
    app_instance = app.instance

    async def override_get_db():
        yield test_db

    app_instance.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app_instance),
        base_url="http://test",
    ) as ac:
        yield ac

    app_instance.dependency_overrides.clear()
