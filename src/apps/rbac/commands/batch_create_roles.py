from typing import Any

from click import Command, Context

from src.apps.rbac.repos.role_repo import RoleRepo
from src.core.database import SessionLocal
from src.utils.constants import DEFAULT_ROLES


class BatchCreateRolesCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        self._batch_create()
        return super().invoke(ctx)

    @staticmethod
    def _batch_create() -> None:
        with SessionLocal() as db:
            try:
                params = []
                for role in DEFAULT_ROLES:
                    params.append({"name": role})

                RoleRepo(db).batch_create(params)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                raise
