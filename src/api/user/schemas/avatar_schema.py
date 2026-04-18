from typing import TypedDict

from pydantic import BaseModel


class AvatarUploadRequest(TypedDict):
    filename: str


class AvatarUploadResponse(TypedDict):
    avatar_put_url: str
    key: str


class AvatarUploadRequestSchema(BaseModel):
    filename: str


class AvatarUploadResponseSchema(BaseModel):
    avatar_put_url: str
    key: str


class AvatarUploadCallbackRequest(TypedDict):
    key: str


class AvatarUploadCallbackResponse(TypedDict):
    avatar_url: str


class AvatarUploadCallbackRequestSchema(BaseModel):
    key: str


class AvatarUploadCallbackResponseSchema(BaseModel):
    avatar_url: str
