from typing import Any

from fastapi.exceptions import HTTPException

from src.apps.auth.models import Demo
from src.apps.auth.repos import DemoRepo
from src.apps.auth.schemas import LoginRequestSchema, RegisterRequestSchema, DemoInfoSchema
from src.utils.datastructures.json_web_token import JSONWebToken


class DemoService:
    def __init__(self, repo: DemoRepo) -> None:
        self.repo = repo

    def login(self, req: LoginRequestSchema) -> Any:
        """
        :param req: login request schema
        :return: tuple | None: (auth instance, access, refresh)
        """
        demo = self.repo.get_demo_by_id(req.id)
        if not demo:
            raise HTTPException(status_code=400, detail="failed to create auth")
        access, refresh = self._generate_token_pair(req=req)
        return demo, access, refresh

    @staticmethod
    def _generate_token_pair(req: LoginRequestSchema) -> tuple[str, str]:
        access = JSONWebToken.create_access_token(id_=req.id)
        refresh = JSONWebToken.create_refresh_token(id_=req.id)
        return access, refresh

    def register(self, req: RegisterRequestSchema) -> Demo:
        """
        :param req:
        :return: auth instance
        """
        return self.repo.create_demo(name=req.name)

    def get_demo_by_id(self, id_: int) -> Demo | None:
        return self.repo.get_demo_by_id(id_=id_)

    @staticmethod
    def get_demo_info_by_model(demo: Demo) -> dict[str, Any]:
        return DemoInfoSchema.model_validate(demo).model_dump()

    @staticmethod
    def get_register_success_info(demo: Demo) -> dict[str, Any]:
        return {"id": demo.id, "msg": "register success, please login"}

    @staticmethod
    def get_login_success_info(demo: Demo, access: str, refresh: str) -> dict[str, Any]:
        return {"msg": "success", "id": demo.id, "access": access, "refresh": refresh}
