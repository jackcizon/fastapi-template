from src.core.db.models import Base
from src.core.resources import resources


def create_all_tables() -> None:  # pragma: no cover
    """useless when dba has already managed db"""
    # from src.api.<api_name>.models import <model_name>

    Base.metadata.create_all(resources.engine)


def drop_all_tables() -> None:  # pragma: no cover
    # from src.api.<api_name>.models import <model_name>

    Base.metadata.drop_all(resources.engine)


if __name__ == "__main__":  # pragma: no cover
    # create_all_tables()
    # drop_all_tables()
    pass
