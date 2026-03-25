from typing import Sequence

from sqlalchemy import text, Result
from sqlalchemy.orm import Session

from src.apps.rbac.models import User


class RbacRepo():
    def __init__(self, db: Session):
        self.db = db

    def get_user_permissions(self, user: User) -> Sequence:
        user_permissions_result: Result = self.db.execute(
            text("""
                            WITH user_roles AS (
                                SELECT ur.user_id, ur.role_id
                                FROM "Rbac_User2Role" ur
                                WHERE ur.user_id = :user_id
                            ),
                            role_permissions AS (
                                SELECT rp.role_id, rp.permission_id
                                FROM "Rbac_Role2Permission" rp
                                WHERE rp.role_id IN (SELECT role_id FROM user_roles)
                            )
                            SELECT p.code
                            FROM "Rbac_Permission" p
                            JOIN role_permissions rp ON rp.permission_id = p.id;
                            """),
            {"user_id": user.id},
        )
        # [('rbac:index',), ('auth:me',), ('auth:register',), ('auth:login',), ...]
        return user_permissions_result.fetchall()
