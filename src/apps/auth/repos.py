from sqlalchemy.orm import Session


class AuthRepo:
    def __init__(self, db: Session | None = None, cursor=None):
        self.db = db
        self.cursor = cursor

