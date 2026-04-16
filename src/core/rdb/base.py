from redis.asyncio.client import Redis

from src.core.resources import resources


async def get_cache() -> Redis:
    return resources.cache


async def get_broker() -> Redis:
    return resources.broker
