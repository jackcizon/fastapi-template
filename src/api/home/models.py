from src.core.db.mixin import IdMixin
from src.core.db.models import Base


class Header(IdMixin, Base):
    pass


class Footer(IdMixin, Base):
    pass
