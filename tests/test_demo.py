"""update to dev branch"""

from src.demo import demo


def test_demo():
    assert demo(1) == 2
