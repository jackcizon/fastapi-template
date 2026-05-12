from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas.register_schema import RegisterRequest, RegisterResponse
from src.api.rbac.repos.role_repo import RoleRepo
from src.api.rbac.repos.user2role_repo import User2RoleRepo
from src.api.rbac.repos.user_repo import UserRepo
from src.api.user.repos.userprofile_repo import UserProfileRepo
from src.core.constants import AUTHED_ROLE
from src.core.exceptions.auth import AuthError
from src.core.cache.keys import cache_keys
from src.core.securities.password import Password
from src.core.services.distributed_ids import unique_id_factory


class RegisterService:
    @staticmethod
    async def register(req: RegisterRequest, db: AsyncSession, cache: Redis) -> RegisterResponse:
        # validate
        email = req["email"]
        if await UserRepo(db).get_one_by_field_eq("email", email):
            raise AuthError("User Exists.")
        verification_code_cache = await cache.get(f"{cache_keys.email_verification_code}:{email}")
        if verification_code_cache != req["verification_code"]:
            raise AuthError("Verification Error.")

        # create instance
        user_id = unique_id_factory()
        params = [{"id": user_id, "name": req["name"], "password": Password.hash(req["password"]), "email": email}]
        await UserRepo(db).batch_create(params)

        # create related instances
        # user role
        role = await RoleRepo(db).get_one_by_field_eq("name", str(AUTHED_ROLE))
        role_id = role.id
        params = [{"user_id": user_id, "role_id": role_id}]
        await User2RoleRepo(db).batch_create(params)

        # userprofile
        params = [{"id": user_id}]
        await UserProfileRepo(db).batch_create(params)

        # response
        return RegisterResponse(message="register success, please login.", status=True)
