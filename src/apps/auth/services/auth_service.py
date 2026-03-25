from sqlalchemy.orm import Session

from src.apps.auth.schemas.login_schema import LoginRequestSchema
from src.apps.rbac.repos.user_repo import UserRepo
from src.utils.datastructures.json_web_token import JSONWebToken
from src.core.exceptions.auth import AuthError
from src.core.securities.password import Password


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
