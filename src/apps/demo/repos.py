"""repos for demos"""

from sqlalchemy.orm import Session

from src.apps.demo.models import Demo


class DemoRepo:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def get_demo_by_id(self, id_: int) -> Demo | None:
        return self.db.query(Demo).filter_by(id=id_).first()

    def create_demo(self, name: str) -> Demo:
        demo = Demo(name=name)
        self.db.add(demo)
        self.db.flush()
        return demo
