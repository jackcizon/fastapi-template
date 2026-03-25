# this map needs to recursion to get the role hierarchy
from typing import Final, Any

ROLE_CHILD_MAP: Final[dict[str, list[Any]]] = {
    # role: [child1, child2] or []
    "user": [],
    "staff": ["user"],
    "finance": ["staff"],
    "cto": ["staff"],
    "ceo": ["finance", "cto"],
    "chairman": ["ceo"],
}

DEFAULT_ROLES: Final[list[str]] = list(ROLE_CHILD_MAP.keys())

DEFAULT_ROLE: Final[str] = DEFAULT_ROLES[0]

PASSED_APP_PERMISSIONS_CHECK: Final[list[str]] = [
    "alembic",
    "migrations",
]  # these apps will ignore permissions update.
