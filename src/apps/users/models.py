from sqlmodel.main import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users_User"
    id: int = Field(None, primary_key=True)
    name: str
    age: int = Field(1, ge=1, le=120, description="age[1, 120]")
    description: str | None = None
