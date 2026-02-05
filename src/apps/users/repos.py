"""repos for users"""

import uuid

from sqlalchemy.orm import Session

from src.apps.users.models import User


class UserRepo:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def get_login_user(self, open_id: str) -> User | None:
        """open-id 是通过请求wechat的api得到的,此处简化"""
        return self.db.query(User).filter_by(open_id=open_id).first()

    def create_user(self, gender: int, nick_name: str) -> User:
        user = User(gender=gender, nick_name=nick_name, open_id=uuid.uuid4().hex)
        self.db.add(user)
        self.db.flush()
        return user
