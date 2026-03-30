from sqlalchemy.orm import Session

from src.api.auth.schemas.refresh_schema import RefreshRequestSchema, RefreshResponseSchema
from src.api.rbac.repos.user_repo import UserRepo
from src.core.exceptions.auth import AuthError
from src.utils.datastructures.json_web_token import JSONWebToken


class RefreshService:
    @staticmethod
    def refresh(req: RefreshRequestSchema, db: Session) -> RefreshResponseSchema:
        payload = JSONWebToken.decode_token(req.refresh, token_type="refresh")
        user_id = payload.get("user_id")
        user = UserRepo(db).get_one_by_field_eq("id", user_id)
        if user is None:
            raise AuthError("User not found.")
        access = JSONWebToken.create_access_token(user_id)
        return RefreshResponseSchema(access=access)
