from typing import TypedDict

from pydantic import BaseModel, Field


class RegisterRequest(TypedDict):
    name: str
    email: str
    password: str
    verification_code: str


class RegisterResponse(TypedDict):
    status: bool
    message: str


class RegisterRequestSchema(BaseModel):  # pragma: no cover
    name: str = Field(min_length=4, max_length=16)
    email: str = Field(min_length=6, max_length=32, pattern=r"^[1-9a-zA-Z][\w\.-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
    password: str = Field(min_length=6, max_length=20)
    verification_code: str = Field(min_length=6, max_length=16)


class RegisterResponseSchema(BaseModel):  # pragma: no cover
    status: bool = False
    message: str
