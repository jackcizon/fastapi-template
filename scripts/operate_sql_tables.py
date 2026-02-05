from src.core.database import Base, engine


def create_all_tables() -> None:  # pragma: no cover
    """useless when dba has already managed db"""
    from src.apps.users.models import User
    # from src.apps.books.models import (
    #     Book,
    #     BookShelf,
    #     BookVolume,
    #     BookCategory,
    #     BookChapter,
    #     BookBigCategory,
    #     BookChapterContent,
    #     BookCategoryRelation,
    # )
    # from src.apps.search.models import SearchKeyWord
    # from src.apps.history.models import BrowseHistory

    Base.metadata.create_all(engine)


def drop_all_tables() -> None:  # pragma: no cover
    from src.apps.users.models import User
    # from src.apps.books.models import (
    #     Book,
    #     BookShelf,
    #     BookVolume,
    #     BookCategory,
    #     BookChapter,
    #     BookBigCategory,
    #     BookChapterContent,
    #     BookCategoryRelation,
    # )
    # from src.apps.search.models import SearchKeyWord
    # from src.apps.history.models import BrowseHistory

    Base.metadata.drop_all(engine)


if __name__ == "__main__":  # pragma: no cover
    create_all_tables()
    # drop_all_tables()
    pass
