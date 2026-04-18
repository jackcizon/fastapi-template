from typing import TypedDict

from pydantic import BaseModel, Field


class PasswordResetRequest(TypedDict):
    new_password: str
    verification_code: str


class PasswordResetResponse(TypedDict):
    status: bool


class PasswordResetRequestSchema(BaseModel):
    new_password: str = Field(min_length=6, max_length=20)
    verification_code: str = Field(min_length=6, max_length=9)


class PasswordResetResponseSchema(BaseModel):
    status: bool = False


class PasswordForgetRequest(TypedDict):
    email: str
    verification_code: str
    new_password: str


class PasswordForgetResponse(TypedDict):
    status: bool


class PasswordForgetRequestSchema(BaseModel):
    email: str = Field(min_length=6, max_length=32, pattern=r"^[1-9a-zA-Z][\w\.-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
    verification_code: str = Field(min_length=6, max_length=9)
    new_password: str = Field(min_length=6, max_length=20)


class PasswordForgetResponseSchema(BaseModel):
    status: bool = False
