from src.core.db.session import Base, engine


def create_all_tables() -> None:  # pragma: no cover
    """useless when dba has already managed db"""
    # from src.apps.<app_name>.models import <model_name>

    Base.metadata.create_all(engine)


def drop_all_tables() -> None:  # pragma: no cover
    # from src.apps.<app_name>.models import <model_name>

    Base.metadata.drop_all(engine)


if __name__ == "__main__":  # pragma: no cover
    # create_all_tables()
    # drop_all_tables()
    pass
