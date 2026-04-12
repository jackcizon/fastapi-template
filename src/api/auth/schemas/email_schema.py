from typing import TypedDict

from pydantic import BaseModel, Field


class EmailVerificationRequest(TypedDict):
    email: str


class EmailVerificationResponse(TypedDict):
    verification_code: str


class EmailVerificationRequestSchema(BaseModel):
    email: str = Field(min_length=6, max_length=32, pattern=r"^[1-9a-zA-Z][\w\.-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")


class EmailVerificationResponseSchema(BaseModel):
    verification_code: str = Field(min_length=6, max_length=32)
