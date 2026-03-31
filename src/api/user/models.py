from src.core.db.mixin import DistributedIdMixin
from src.core.db.models import BaseModel


class UserProfile(DistributedIdMixin, BaseModel):
    pass
