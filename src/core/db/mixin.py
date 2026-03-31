from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.core.services.distributed_ids import unique_id_factory


class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class DistributedIdMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=unique_id_factory)
