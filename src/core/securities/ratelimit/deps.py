from fastapi import HTTPException
from fastapi.params import Depends
from redis.asyncio import Redis
from starlette.requests import Request

from src.core.rdb.base import get_cache
from src.core.rdb.keys import cache_keys
from src.core.securities.ratelimit.token_bucket import RedisTokenBucketRatelimiter


class RateLimitDep:
    def __init__(self, limit: int, period: float):
        self.limit = limit
        self.period = period

    async def __call__(self, request: Request, cache: Redis = Depends(get_cache)) -> None:
        key = f"{cache_keys.ratelimit}:{request.client.host}"

        limiter = RedisTokenBucketRatelimiter(cache=cache, limit=self.limit, period=self.period)

        if not await limiter.allow(key):
            raise HTTPException(429, "Too Many Requests")
