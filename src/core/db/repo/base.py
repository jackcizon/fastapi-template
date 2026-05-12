from typing import Any, Generic, Sequence

from sqlalchemy import delete, select, Update, func, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.types import Model


class BaseRepo(Generic[Model]):
    def __init__(self, db: AsyncSession, /, *, model: type[Model] = None) -> None:
        self.db = db
        self.model = model

    def column(self, field: str) -> Any:
        return getattr(self.model, field)


class QueryRepo(BaseRepo[Model]):
    """select"""

    async def get_one_by_field_eq(self, field: str, val: Any) -> Model | None:
        stat = select(self.model).where(self.column(field) == val)  # type: ignore
        res = await self.db.execute(stat)
        return res.scalars().first()

    async def get_all(self) -> Sequence[Model]:
        stat = select(self.model)
        res = await self.db.execute(stat)
        return res.scalars().all()

    async def get_all_by_field_eq(self, field: str, val: str) -> Sequence[Model]:
        stat = select(self.model).where(self.column(field) == val)  # type: ignore
        res = await self.db.execute(stat)
        return res.scalars().all()

    async def get_all_by_field_in(self, field: str, vals: list[str]) -> Sequence[Model]:
        col = getattr(self.model, field)
        stat = select(self.model).where(col.in_(vals))
        res = await self.db.execute(stat)
        return res.scalars().all()

    async def count(self) -> int:
        stat = select(func.count(self.model.id))
        res = await self.db.execute(stat)
        return res.scalar()

    async def get_all_paginated(self, offset: int, limit: int) -> Any:
        raise NotImplementedError


class ModifyRepo(BaseRepo[Model]):
    """update, delete, insert"""

    async def update(self, where: Any, fields: dict) -> None:
        stat = Update(self.model).where(where).values(**fields)
        await self.db.execute(stat)

    async def delete(self, where: Any) -> None:
        stat = Delete(self.model).where(where)
        await self.db.execute(stat)

    async def del_all(self) -> None:
        stat = delete(self.model).where(self.column("id") > 0)
        await self.db.execute(stat)


class CrudRepo(QueryRepo[Model], ModifyRepo[Model]):
    """crud"""

    async def execute_stat_params(self, stat: Any, params: list[dict[str, Any]] = None) -> Any:
        return await self.db.execute(stat, params)
