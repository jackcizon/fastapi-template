import os
import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from redis.asyncio import Redis
from sqlalchemy import NullPool

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import Settings
from src.core.db.models import Base
from src.core.db.session import get_db
from src.core.cache.base import get_cache, get_broker
from src.main import app

test_settings = Settings("test")

# use asyncpg
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", test_settings.database_url)  # ci docker test db
if TEST_DATABASE_URL.startswith("postgresql://"):
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif TEST_DATABASE_URL.startswith("postgresql+psycopg2://"):
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)


@pytest.fixture
async def test_cache():
    client = Redis.from_url(url=os.getenv("TEST_CACHE_REDIS_URL", test_settings.cache_url), decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


@pytest.fixture
async def test_broker():
    client = Redis.from_url(url=os.getenv("TEST_BROKER_REDIS_URL", test_settings.broker_url), decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


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
async def test_client(test_db, test_cache, test_broker):
    app_instance = app.instance

    async def override_get_db():
        yield test_db

    async def override_get_cache():
        yield test_cache

    async def override_get_broker():
        yield test_broker

    app_instance.dependency_overrides[get_db] = override_get_db
    app_instance.dependency_overrides[get_cache] = override_get_cache
    app_instance.dependency_overrides[get_broker] = override_get_broker

    async with AsyncClient(
        transport=ASGITransport(app=app_instance),
        base_url="http://test",
    ) as ac:
        yield ac

    app_instance.dependency_overrides.clear()
