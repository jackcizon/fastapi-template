"""global fixtures"""

from collections.abc import Generator
from functools import partial

import pytest
from sqlalchemy import create_engine, StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session

from src.main import app
from src.core.db.models import Base
from src.core.db.session import get_db

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestSessionLocal = sessionmaker(bind=engine)


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
    session = TestSessionLocal()

    try:
        yield session
        # must commit in test functions
        # In the test function, `commit` will immediately assert.
        # otherwise, it will cause an assertion error inside the function.
        # session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
        # del tables data
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())


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
