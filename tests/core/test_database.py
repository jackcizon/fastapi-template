"""tests for core:database"""

from sqlalchemy.orm import Session

from src.core.database import get_session


def test_get_session():
    # 创建 generator
    gen = get_session()

    # 取出 yield 的 session
    session = next(gen)

    # 断言类型正确
    assert isinstance(session, Session)

    # 关闭 generator，保证 coverage 完整
    try:
        next(gen)
    except StopIteration:
        pass
