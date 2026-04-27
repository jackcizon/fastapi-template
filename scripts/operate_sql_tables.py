import asyncio

from src.core.resources import resources
from src.api.models import *


async def create_all_tables() -> None:  # pragma: no cover
    """useless when dba has already managed db"""
    await resources.init()
    async with resources.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:  # pragma: no cover
    await resources.init()
    async with resources.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(create_all_tables())
    # asyncio.run(drop_all_tables())
    pass
