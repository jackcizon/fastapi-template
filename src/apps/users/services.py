from typing import Any

from src.apps.users.models import User
from src.apps.users.repos import UserRepo
from src.apps.users.schemas import LoginRequestSchema, RegisterRequestSchema, UserInfoSchema
from src.utils.datastructures import JSONWebToken
from src.utils.exceptions import NotFoundError


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    def login(self, req: LoginRequestSchema) -> Any:
        """
        :param req: login request schema
        :return: tuple | None: (user instance, access, refresh)
        """
        user = self.repo.get_login_user(open_id=req.open_id)
        if not user:
            # 万一事务失败也抛异常
            raise NotFoundError("failed to create user")
        access, refresh = self._generate_token_pair(req=req)
        return user, access, refresh

    @staticmethod
    def _generate_token_pair(req: LoginRequestSchema) -> tuple[str, str]:
        access = JSONWebToken.create_access_token(id_=req.open_id)
        refresh = JSONWebToken.create_refresh_token(id_=req.open_id)
        return access, refresh

    def register(self, req: RegisterRequestSchema) -> User:
        """
        :param req:
        :return: user instance
        """
        return self.repo.create_user(nick_name=req.nick_name, gender=req.gender)

    def get_user_by_open_id(self, open_id: str) -> User | None:
        return self.repo.get_login_user(open_id=open_id)

    @staticmethod
    def get_user_info_by_model(user: User) -> dict[str, Any]:
        return UserInfoSchema.model_validate(user).model_dump()

    @staticmethod
    def get_register_success_info(user: User) -> dict[str, Any]:
        return {"id": user.id, "msg": "register success, please login"}

    @staticmethod
    def get_login_success_info(user: User, access: str, refresh: str) -> dict[str, Any]:
        return {"msg": "success", "id": user.id, "access": access, "refresh": refresh}
