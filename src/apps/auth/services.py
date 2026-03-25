from sqlalchemy.orm import Session

from src.apps.rbac.repos import UserRepo
from src.apps.auth.schemas import LoginRequestSchema
from src.utils.datastructures.json_web_token import JSONWebToken
from src.utils.exceptions.auth import AuthError
from src.utils.securities.password import Password


class AuthService:
    @staticmethod
    def login(req: LoginRequestSchema, db: Session) -> tuple[str, str]:
        """
        :return: tuple(access, refresh) or None
        """
        user = UserRepo(db).get_user_by_email(req.email)
        if user is None or not Password.verify(req.password, user.get("password")):
            raise AuthError()
        return JSONWebToken.generate_token_pair(user.get("id"))
