from pydantic import BaseModel, Field


class LoginRequestSchema(BaseModel):
    id: int


class RegisterRequestSchema(BaseModel):
    name: str


class DemoInfoSchema(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}
