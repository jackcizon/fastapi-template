from typing import TypedDict

from pydantic import BaseModel


class MeRequest(TypedDict):
    pass


class MeResponse(TypedDict):
    user_id: int
    avatar: str


class MeRequestSchema(BaseModel):
    pass


class MeResponseSchema(BaseModel):
    user_id: int
    avatar: str
