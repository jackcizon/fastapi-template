"""config for database"""

from typing import Generator

from sqlmodel.main import SQLModel
from sqlalchemy.engine.create import create_engine
from sqlmodel.orm.session import Session

from src.core.config import infra_settings

engine = create_engine(infra_settings.DATABASE_URL)


def create_db_and_tables() -> None:
    """useless when dba has already managed db"""
    # from src.apps.users.models import User

    SQLModel.metadata.create_all(engine)  # pragma: no cover


def get_session() -> Generator:
    """yield a db session"""
    with Session(engine) as session:
        yield session
