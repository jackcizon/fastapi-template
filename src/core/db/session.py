from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
AsyncSessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as db:
        try:
            yield db
            await db.commit()  # comment this line if you want to manually commit in `with` code block
        except Exception as e:
            await db.rollback()
            print(e)
            raise  # any exceptions
        finally:
            await db.close()
