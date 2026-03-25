from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
# session factory
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
