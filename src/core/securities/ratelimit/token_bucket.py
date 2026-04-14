import os
import time
from typing import LiteralString

from ratelimiter_lite.base import BaseRateLimiter
from redis.asyncio import Redis

from src.core.config import SRC_DIR


class RedisTokenBucketRatelimiter(BaseRateLimiter):
    def __init__(self, cache: Redis, limit: int, period: float) -> None:
        super().__init__(limit, period)
        self._rate = limit / period
        self._cache = cache
        self._lua_script = self._read_lua_script()

    async def allow(self, key: str) -> bool:
        result = await self._cache.eval(self._lua_script, 1, key, self._limit, self._rate, time.monotonic(), 1)
        return bool(result)

    @staticmethod
    def _read_lua_script(
        path: LiteralString | str = os.path.join(SRC_DIR, "core/securities/ratelimit/script.lua"),
    ) -> str:
        fd = os.open(path, os.O_RDONLY)
        size = os.lseek(fd, 0, os.SEEK_END)
        os.lseek(fd, 0, os.SEEK_SET)
        content = os.read(fd, size).decode()
        return content
