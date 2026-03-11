from sqlalchemy import Column, String

from src.utils.models import BaseModel


class User(BaseModel):
    name = Column(String(50))
    __tablename__ = "User"
