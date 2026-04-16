from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.resources import resources


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with resources.session_factory() as db:
        try:
            yield db
            await db.commit()  # comment this line if you want to manually commit in `with` code block
        except Exception as e:
            await db.rollback()
            print(e)
            raise  # any exceptions
        finally:
            await db.close()
