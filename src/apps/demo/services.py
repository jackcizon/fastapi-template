from typing import Any

from fastapi.exceptions import HTTPException

from src.apps.demo.models import User
from src.apps.demo.repos import UserRepo
from src.apps.demo.schemas import LoginRequestSchema, RegisterRequestSchema, UserInfoSchema
from src.utils.datastructures import JSONWebToken


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    def login(self, req: LoginRequestSchema) -> Any:
        """
        :param req: login request schema
        :return: tuple | None: (user instance, access, refresh)
        """
        user = self.repo.get_user_by_id(req.id)
        if not user:
            raise HTTPException(status_code=400, detail="failed to create user")
        access, refresh = self._generate_token_pair(req=req)
        return user, access, refresh

    @staticmethod
    def _generate_token_pair(req: LoginRequestSchema) -> tuple[str, str]:
        access = JSONWebToken.create_access_token(id_=req.id)
        refresh = JSONWebToken.create_refresh_token(id_=req.id)
        return access, refresh

    def register(self, req: RegisterRequestSchema) -> User:
        """
        :param req:
        :return: user instance
        """
        return self.repo.create_user(name=req.name)

    def get_user_by_id(self, id_: int) -> User | None:
        return self.repo.get_user_by_id(id_=id_)

    @staticmethod
    def get_user_info_by_model(user: User) -> dict[str, Any]:
        return UserInfoSchema.model_validate(user).model_dump()

    @staticmethod
    def get_register_success_info(user: User) -> dict[str, Any]:
        return {"id": user.id, "msg": "register success, please login"}

    @staticmethod
    def get_login_success_info(user: User, access: str, refresh: str) -> dict[str, Any]:
        return {"msg": "success", "id": user.id, "access": access, "refresh": refresh}
