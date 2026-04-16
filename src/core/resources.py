from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine


class ResourceManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory = None
        self.cache: Redis | None = None
        self.broker: Redis | None = None

    async def init(self, db_url: str, cache_url: str, broker_url: str) -> None:
        self.engine = create_async_engine(db_url, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        self.cache = Redis.from_url(url=cache_url, decode_responses=True)
        self.broker = Redis.from_url(url=broker_url, decode_responses=True)

    async def aclose(self) -> None:
        if self.engine:
            await self.engine.dispose()
        if self.cache:
            await self.cache.aclose()
        if self.broker:
            await self.broker.aclose()


resources = ResourceManager()
