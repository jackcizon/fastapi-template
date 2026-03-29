"""global fixtures"""

import os
from collections.abc import Generator
from functools import partial

import pytest
from sqlalchemy import create_engine, event
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session

from src.main import app
from src.core.db.models import Base
from src.core.db.session import get_db

# Hint: when test config becomes complex, use json as config.
# 1. is there exists an env var:TEST_DATABASE_URL?
# 2. if has(in CI)，just use it.
# 3. if not exists,(in local), use private ip 192.168.x.x
SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+psycopg2://jack:jack021213@192.168.8.7:5433/test_fastapi_template"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# global fixture
# _ScopeName = Literal["session", "package", "module", "class", "function"]
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db() -> Generator[Session, None, None]:
    """class Generator(Iterator[_YieldT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co]):"""
    connection = engine.connect()
    transaction = connection.begin()

    session = TestSessionLocal(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session_, transaction_):
        if transaction_.nested and not transaction_._parent.nested:
            session_.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def override_get_db(db: Session) -> Generator[Session, None, None]:
    try:
        yield db
    finally:
        pass


@pytest.fixture
def test_client(test_db: Session) -> Generator[TestClient, None, None]:
    """test client factory

    # e.g.:
    from functools import partial

    def get_name(name: str):
        return name

    get_jack = partial(name, "jack")  # froze `name` to "jack"

    if __name__ == '__main__':
        print(get_jack())
    """

    # use test db
    # froze to `test_db`
    app_instance = app.instance

    app_instance.dependency_overrides[get_db] = partial(override_get_db, test_db)

    with TestClient(app_instance) as client:
        yield client

    app_instance.dependency_overrides.clear()
