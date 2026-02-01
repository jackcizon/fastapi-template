"""repos for users"""

from sqlalchemy.orm import Session


class UserRepo:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def get_all(self) -> dict:
        # return self.db.query(User).all()
        return {"1": "jack", "2": "john"}

    #
    # def get_by_id(self, user_id: int):
    #     return self.db.query(User).filter(User.id == user_id).first()
    #
    # def create(self, user: User):
    #     self.db.add(user)
    #     self.db.commit()
    #     self.db.refresh(user)
    #     return user
