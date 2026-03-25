from typing import Sequence

from sqlalchemy import select, text, Result
from sqlalchemy.orm import Session

from src.apps.rbac.models import User, User2Role, Role2Permission, Permission
from src.core.db.repo.base import BaseRepo


class RbacRepo(BaseRepo):
    def __init__(self, db: Session):
        super().__init__(db)
        self.user = User
        self.permission = Permission
        self.user_role = User2Role
        self.role_permission = Role2Permission

    def get_user_permissions(self, user: User) -> Sequence:
        # user_permissions_result: Result = self.db.execute(
        #     text("""
        #                     WITH user_roles AS (
        #                         SELECT ur.user_id, ur.role_id
        #                         FROM "Rbac_User2Role" ur
        #                         WHERE ur.user_id = :user_id
        #                     ),
        #                     role_permissions AS (
        #                         SELECT rp.role_id, rp.permission_id
        #                         FROM "Rbac_Role2Permission" rp
        #                         WHERE rp.role_id IN (SELECT role_id FROM user_roles)
        #                     )
        #                     SELECT p.code
        #                     FROM "Rbac_Permission" p
        #                     JOIN role_permissions rp ON rp.permission_id = p.id;
        #                     """),
        #     {"user_id": user.id},
        # )
        # # [('rbac:index',), ('auth:me',), ('auth:register',), ('auth:login',), ...]
        # return user_permissions_result.fetchall()

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
        return self.db.execute(stat).scalars().all()
