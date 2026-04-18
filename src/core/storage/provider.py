from typing import Protocol, runtime_checkable

from src.core.config import settings
from src.core.resources import resources


@runtime_checkable
class StorageProviderInterface(Protocol):
    def get_url(self, path: str) -> str: ...


class LocalStorage:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_url(self, path: str) -> str:
        return f"{self.base_url}/{path}"


class S3Storage:
    def __init__(self, endpoint: str = settings.s3_endpoint, bucket: str = settings.s3_bucket) -> None:
        self.endpoint = endpoint
        self.bucket = bucket

    def get_url(self, object_key: str) -> str:
        s3 = resources.s3_session.client("s3", endpoint_url=self.endpoint)

        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket,
                "Key": object_key,  # query from db, e.g.: get UserProfile.avatar -> s3 server -> image
            },
            ExpiresIn=3600,
        )
        return url
