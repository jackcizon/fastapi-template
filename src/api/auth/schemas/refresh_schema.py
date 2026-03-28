from pydantic import BaseModel, Field


class RefreshRequestSchema(BaseModel):
    refresh: str


class RefreshResponseSchema(BaseModel):
    access: str
