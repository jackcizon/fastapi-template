from redis.asyncio.client import Redis

from src.core.config import settings

cache = Redis(
    host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, decode_responses=True
)
