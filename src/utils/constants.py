# this map needs to recursion to get the role hierarchy
ROLE_CHILD_MAP = {
    # role: [child1, child2] or []
    "user": [],
    "staff": ["user"],
    "finance": ["staff"],
    "cto": ["staff"],
    "ceo": ["finance", "cto"],
    "chairman": ["ceo"],
}

PASSED_APP_PERMISSIONS_CHECK = ["authentication"]  # these apps will ignore permissions update.

DEFAULT_ROLE = "user"
