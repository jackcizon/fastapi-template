from redis.asyncio.client import Redis

from src.core.config import settings

cache = Redis(
    host=settings.cache_host, port=settings.cache_port, password=settings.cache_password, decode_responses=True
)
