from typing import TypedDict

from pydantic import BaseModel


class RefreshRequest(TypedDict):
    refresh: str


class RefreshResponse(TypedDict):
    access: str


class RefreshRequestSchema(BaseModel):
    refresh: str


class RefreshResponseSchema(BaseModel):
    access: str
