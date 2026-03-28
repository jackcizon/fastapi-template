from sqlalchemy.orm import Session

from src.api.auth.schemas.login_schema import LoginRequestSchema, LoginResponseSchema
from src.api.rbac.repos.user_repo import UserRepo
from src.utils.datastructures.json_web_token import JSONWebToken
from src.core.exceptions.auth import AuthError
from src.core.securities.password import Password


class LoginService:
    @staticmethod
    def login(req: LoginRequestSchema, db: Session) -> LoginResponseSchema:
        """
        :return: tuple(access, refresh) or None
        """
        user = UserRepo(db).get_user_by_email(req.email)
        if user is None or not Password.verify(req.password, user.get("password")):
            raise AuthError("Auth Failed")
        access, refresh = JSONWebToken.generate_token_pair(user.get("id"))
        return LoginResponseSchema(access=access, refresh=refresh)
