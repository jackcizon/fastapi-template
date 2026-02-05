from pydantic import BaseModel, Field


class LoginRequestSchema(BaseModel):
    """登录需要结合wechat,此处简化不再验证"""

    open_id: str = Field(
        max_length=128, description="wechat open-id, 这里采用模拟通过了微信登录验证,open-id不用校验"
    )


class RegisterRequestSchema(BaseModel):
    """为了简化,不再验证字段"""

    nick_name: str | None
    gender: int
    # others


class UserInfoSchema(BaseModel):
    nick_name: str
    gender: int
    # 还有很多...

    model_config = {
        "from_attributes": True  # 允许从 ORM / 对象读取属性
    }
