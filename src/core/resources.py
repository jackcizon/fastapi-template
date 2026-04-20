from boto3 import Session
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from src.core.config import settings


class ResourceManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory = None
        self.cache: Redis | None = None
        self.broker: Redis | None = None
        self.s3_session: Session | None = None

    async def init(
        self,
        db_url: str = settings.database_url,
        cache_url: str | None = None,
        broker_url: str | None = None,
        s3_region: str | None = None,
        s3_access_key_id: str | None = None,
        s3_access_key_secret: str | None = None,
    ) -> None:
        if db_url:
            self.engine = create_async_engine(db_url, pool_pre_ping=True)
            self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        if cache_url:
            self.cache = Redis.from_url(url=cache_url, decode_responses=True)
        if broker_url:
            self.broker = Redis.from_url(url=broker_url, decode_responses=True)
        if s3_region and s3_access_key_id and s3_access_key_secret:
            self.s3_session = Session(
                region_name=s3_region, aws_access_key_id=s3_access_key_id, aws_secret_access_key=s3_access_key_secret
            )

    async def aclose(self) -> None:
        if self.engine:
            await self.engine.dispose()
        if self.cache:
            await self.cache.aclose()
        if self.broker:
            await self.broker.aclose()


resources = ResourceManager()
