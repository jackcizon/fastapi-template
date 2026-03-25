from typing import Generator

from src.core.db.session import SessionLocal


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
