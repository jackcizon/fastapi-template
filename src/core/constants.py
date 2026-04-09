# this map needs to recursion to get the role hierarchy
from enum import StrEnum
from typing import Final


# CONFIG AS CODE
# TODO: Replace with your Rbac Roles under this line.
class ROLE(StrEnum):
    VISITOR = "visitor"
    USER = "user"
    STAFF = "staff"
    FINANCE = "finance"
    CTO = "cto"
    CEO = "ceo"
    CHAIRMAN = "chairman"


ROLE_CHILD_MAP = {
    # role: [child1, child2] or []
    ROLE.VISITOR.value: [],  # not login user
    ROLE.USER.value: [ROLE.VISITOR.value],
    ROLE.STAFF.value: [ROLE.USER.value],
    ROLE.FINANCE.value: [ROLE.STAFF.value],
    ROLE.CTO.value: [ROLE.STAFF.value],
    ROLE.CEO.value: [ROLE.FINANCE.value, ROLE.CTO.value],
    ROLE.CHAIRMAN.value: [ROLE.CEO.value],
}

DEFAULT_ROLES = [str(role.value) for role in ROLE]

DEFAULT_ROLE = ROLE.VISITOR.value

PASSED_APP_PERMISSIONS_CHECK: Final[list[str]] = [
    "alembic",
    "migrations",
]  # these api will ignore permissions update.
