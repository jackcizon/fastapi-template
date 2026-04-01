from typing import NamedTuple  # pragma: no cover


class PermissionInfo(NamedTuple):  # pragma: no cover
    role: str
    code: str
    role_parents_set: set
