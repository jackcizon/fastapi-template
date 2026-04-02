from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import User, User2Role, Role2Permission, Permission
from src.core.db.repo.base import BaseRepo
from src.core.types import Model


class RbacRepo(BaseRepo[Model]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)
        self.user = User
        self.permission = Permission
        self.user_role = User2Role
        self.role_permission = Role2Permission

    async def get_user_permissions(self, user: User) -> Sequence[Model]:
        user_roles = (
            select(self.user_role.user_id, self.user_role.role_id)
            .where(self.user_role.user_id == user.id)  # type: ignore
            .cte("user_roles")
        )

        # .c is .column
        role_permissions = (
            select(self.role_permission.role_id, self.role_permission.permission_id)
            .where(self.role_permission.role_id.in_(select(user_roles.c.role_id)))
            .cte("role_permissions")
        )

        stat = select(self.permission.code).join(
            role_permissions,
            role_permissions.c.permission_id == self.permission.id,  # type: ignore
        )
        res = await self.db.execute(stat)
        return res.scalars().all()
