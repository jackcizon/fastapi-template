from typing import NamedTuple


class PermissionInfo(NamedTuple):
    code: str
    role_parents_set: set
