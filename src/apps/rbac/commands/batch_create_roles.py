from typing import Any

from click import Command, Context

from src.apps.rbac.repos import RoleRepo
from src.apps.rbac.services import RoleService
from src.core.database import SessionLocal


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
                RoleService(RoleRepo(db)).batch_create()
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                raise
