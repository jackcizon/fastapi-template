from typing import Any

from sqlalchemy import Insert


class BatchCreateMixin:
    async def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)  # type: ignore
        await self.db.execute(stat, params)  # type: ignore
