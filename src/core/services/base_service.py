from typing import Any

from src.core.db.base_repo import BaseRepo


class BaseService:
    def __init__(self, repo: BaseRepo) -> None:
        self.repo = repo

    def batch_create(self, stat: Any = None, params: list = None) -> None:
        self.repo.batch_create(stat, params)
