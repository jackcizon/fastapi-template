from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas.login_schema import LoginRequest, LoginResponse
from src.api.rbac.repos.user_repo import UserRepo
from src.utils.datastructures.json_web_token import JSONWebToken
from src.core.exceptions.auth import AuthError
from src.core.securities.password import Password


class LoginService:
    @staticmethod
    async def login(login_request: LoginRequest, db: AsyncSession) -> LoginResponse:
        """
        login service receives a dict, return a dict,
        it does not know what `Pydantic` is.
        all programming lang in same way.

        My Service layer follows the Dependency Inversion Principle (DIP).
        It should not depend on a specific serialization library (Pydantic).
        Data flows through the domain layer using the most general data structure (Dict/TypedDict),
        which guarantees the atomicity and portability of business logic.
        Validation is the responsibility of the infrastructure layer and should not pollute the domain model.

        # TODO: use typing.TypedDict to keep data safe.
        """
        user = await UserRepo(db).get_one_by_field_eq("email", login_request["email"])
        if user is None or not Password.verify(login_request["password"], user.password):
            raise AuthError("Auth Failed")
        access, refresh = JSONWebToken.generate_token_pair(user.id)
        return {"access": access, "refresh": refresh}
