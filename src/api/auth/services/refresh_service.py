from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas.refresh_schema import RefreshRequest
from src.api.rbac.repos.user_repo import UserRepo
from src.core.exceptions.auth import AuthError
from src.utils.datastructures.json_web_token import JSONWebToken


class RefreshService:
    @staticmethod
    async def refresh(req_dict: RefreshRequest, db: AsyncSession) -> dict[str, Any]:
        """
        TODO: use TypedDict to wrap payload, refresh_dict
        """
        payload = JSONWebToken.decode_token(req_dict["refresh"], token_type="refresh")
        user_id = payload.get("user_id")
        user = await UserRepo(db).get_one_by_field_eq("id", user_id)
        if user is None:
            raise AuthError("User not found.")
        access = JSONWebToken.create_access_token(user_id)
        return {"access": access}
