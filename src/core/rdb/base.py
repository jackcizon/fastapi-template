from redis.asyncio.client import Redis

from src.core.config import settings

cache = Redis(
    host=settings.cache_host, port=settings.cache_port, password=settings.cache_password, decode_responses=True
)

broker = Redis(
    host=settings.broker_host, port=settings.broker_port, password=settings.broker_password, decode_responses=True
)


async def get_cache() -> Redis:
    return cache


async def get_broker() -> Redis:
    return broker
