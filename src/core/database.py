"""config for database"""

from typing import Generator

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import infra_settings


class Base(DeclarativeBase):
    pass


engine = create_engine(infra_settings.DATABASE_URL, pool_pre_ping=True)

# session factory
SessionLocal = sessionmaker(engine)


def create_db_and_tables() -> None:  # pragma: no cover
    """useless when dba has already managed db"""
    from src.apps.users.models import User
    from src.apps.books.models import (
        Book,
        BookShelf,
        BookVolume,
        BookCategory,
        BookChapter,
        BookBigCategory,
        BookChapterContent,
        BookCategoryRelation,
    )
    from src.apps.search.models import SearchKeyWord
    from src.apps.history.models import BrowseHistory

    Base.metadata.create_all(engine)


def drop_all_tables() -> None:  # pragma: no cover
    from src.apps.users.models import User
    from src.apps.books.models import (
        Book,
        BookShelf,
        BookVolume,
        BookCategory,
        BookChapter,
        BookBigCategory,
        BookChapterContent,
        BookCategoryRelation,
    )
    from src.apps.search.models import SearchKeyWord
    from src.apps.history.models import BrowseHistory

    Base.metadata.drop_all(engine)


def get_db() -> Generator:
    """db deps"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise  # any exceptions
    finally:
        db.close()
