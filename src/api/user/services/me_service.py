from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.repos.userprofile_repo import UserProfileRepo
from src.api.user.schemas.me_schema import MeResponse
from src.core.storage.provider import S3Storage


class MeService:
    @staticmethod
    async def home_page(user_id: int, db: AsyncSession) -> MeResponse:
        userprofile = await UserProfileRepo(db).get_one_by_field_eq("id", user_id)
        avatar_path = S3Storage().get_url(str(userprofile.avatar))
        return MeResponse(user_id=user_id, avatar=avatar_path)
