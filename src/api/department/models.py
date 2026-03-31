from sqlalchemy.dialects.postgresql import insert

from src.core.db.mixin import DistributedIdMixin
from src.core.db.models import BaseModel
from src.core.db.session import SessionLocal


class Department(DistributedIdMixin, BaseModel):
    __tablename__ = "Department"


if __name__ == "__main__":
    with SessionLocal() as db:
        stat = insert(Department).returning(Department)
        res = db.execute(stat).scalar()
        db.commit()
        print(res.id)
