"""config for database"""

import contextlib
from typing import Generator

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
# session factory
SessionLocal = sessionmaker(engine)


@contextlib.contextmanager
def get_db() -> Generator:
    """
    A Route/Script(with Depends()/ContextManager() -> context) -> Service -> Repo -> DB

    call it in routes via `db = Depends(get_db)`.
    or
    call it in scripts via `with get_db() as db:`.

    `with SessionLocal() as db:` is not recommend usually, because you need to manually manage `try, except, finally`.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # comment this line if you want to manually commit in `with` code block
    except Exception as e:
        print(e)
        db.rollback()
        raise  # any exceptions
    finally:
        db.close()


class Base(DeclarativeBase):
    pass
