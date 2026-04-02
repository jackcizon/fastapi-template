from typing import TypedDict

from pydantic import BaseModel, Field


class LoginRequest(TypedDict):
    email: str
    password: str


class LoginResponse(TypedDict):
    access: str
    refresh: str


class LoginRequestSchema(BaseModel):
    email: str = Field(min_length=6, max_length=32, pattern=r"^[1-9a-zA-Z][\w\.-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
    password: str = Field(min_length=6, max_length=32)


class LoginResponseSchema(BaseModel):
    access: str
    refresh: str
