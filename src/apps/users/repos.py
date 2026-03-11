"""repos for users"""

from sqlalchemy.orm import Session

from src.apps.users.models import User


class UserRepo:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def get_user_by_id(self, id_: int) -> User | None:
        return self.db.query(User).filter_by(id=id_).first()

    def create_user(self, name: str) -> User:
        user = User(name=name)
        self.db.add(user)
        self.db.flush()
        return user
