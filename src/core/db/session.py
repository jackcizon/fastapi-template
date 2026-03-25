from collections.abc import Generator

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
# session factory
SessionLocal = sessionmaker(engine)


def get_db() -> Generator:
    """
    A Route(with Depends() -> context)---------\
                                                =====> Service -> Repo -> DB
    A Script(with SessionLocal() -> context)---/

    call it in routes via `db = Depends(get_db)`.

    `with SessionLocal() as db:` is not recommend usually, because you need to manually manage `try, except, finally`,
    or use it in scripts.
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
