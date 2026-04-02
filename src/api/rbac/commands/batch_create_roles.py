from typing import Any

from click import Command, Context

from src.api.rbac.repos.role_repo import RoleRepo
from src.core.db.session import AsyncSessionFactory
from src.core.constants import DEFAULT_ROLES


class BatchCreateRolesCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def invoke(self, ctx: Context) -> Any:
        await self._batch_create()
        return super().invoke(ctx)

    @staticmethod
    async def _batch_create() -> None:
        async with AsyncSessionFactory() as db:
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
