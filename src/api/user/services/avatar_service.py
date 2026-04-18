from uuid import uuid4

from botocore.config import Config
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.models import UserProfile
from src.api.user.repos.userprofile_repo import UserProfileRepo
from src.api.user.schemas.avatar_schema import (
    AvatarUploadCallbackRequest,
    AvatarUploadCallbackResponse,
    AvatarUploadRequest,
    AvatarUploadResponse,
)
from src.core.config import settings
from src.core.exceptions.auth import AuthError
from src.core.resources import resources
from src.core.storage.provider import S3Storage


class AvatarService:
    @staticmethod
    async def upload(req: AvatarUploadRequest, user_id: int) -> AvatarUploadResponse:
        filename = req["filename"]
        try:
            file_ext = filename.split(".")[-1]
            if file_ext not in ["png", "jpeg", "jpg"]:
                raise AuthError("Invalid File Type.")
        except Exception as e:
            print(e)
            raise AuthError("Invalid File Type")

        file_uuid = uuid4().hex
        object_name = f"user/{user_id}/avatar/{file_uuid}.png"

        client = resources.s3_session.client(
            service_name="s3",
            endpoint_url=settings.s3_endpoint,
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        )

        avatar_put_url = client.generate_presigned_url(
            "put_object",
            Params={"Bucket": settings.s3_bucket, "Key": object_name, "ContentType": "image/png"},
            ExpiresIn=3600,
        )

        return AvatarUploadResponse(avatar_put_url=avatar_put_url, key=object_name)

    @staticmethod
    async def upload_callback(
        req: AvatarUploadCallbackRequest, user_id: int, db: AsyncSession
    ) -> AvatarUploadCallbackResponse:
        key = req["key"]
        if not key.startswith(f"user/{user_id}"):
            raise AuthError("Invalid Key.")

        obj = resources.s3_session.client(
            service_name="s3",
            endpoint_url=settings.s3_endpoint,
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        ).head_object(Bucket=settings.s3_bucket, Key=key)
        if not obj:
            raise AuthError("Key not Exists.")

        await UserProfileRepo(db).update(UserProfile.id == user_id, {"avatar": key})
        avatar_url = S3Storage(endpoint=settings.s3_endpoint, bucket=settings.s3_bucket).get_url(object_key=key)

        return AvatarUploadCallbackResponse(avatar_url=avatar_url)
