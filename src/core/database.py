"""config for database"""

from typing import Generator

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
# session factory
SessionLocal = sessionmaker(engine)


def get_db() -> Generator:
    """db deps"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise  # any exceptions
    finally:
        db.close()


class Base(DeclarativeBase):
    pass
