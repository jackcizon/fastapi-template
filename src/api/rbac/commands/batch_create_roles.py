import asyncio
from typing import Any

from click import Command, Context

from src.api.rbac.repos.role_repo import RoleRepo
from src.core.constants import DEFAULT_ROLES
from src.core.resources import resources


class BatchCreateRolesCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        asyncio.run(self._invoke())
        return super().invoke(ctx)

    async def _invoke(self) -> Any:
        await self._batch_create()

    @staticmethod
    async def _batch_create() -> None:
        await resources.init()
        async with resources.session_factory() as db:
            try:
                params = []
                for role in DEFAULT_ROLES:
                    params.append({"name": role})

                await RoleRepo(db).batch_create(params)
                await db.commit()
            except Exception as e:
                print(e)
                await db.rollback()
                raise
