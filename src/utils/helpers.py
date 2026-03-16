def get_superior_roles(role_name: str, role_map: dict[str, list[str]]):
    """
    input role_name and map, get a set of role and its parents.

    ROLE_CHILD_MAP = {
        # role: [child1, child2] or []
        'user': [],
        'staff': ['user'],
        'finance': ['staff'],
        'cto': ['staff'],
        'ceo': ['finance', 'cto'],
        'chairman': ['ceo'],
    }
    """
    superiors = {role_name}
    for key, value in role_map.items():
        if role_name in value:
            s = get_superior_roles(key, role_map)
            superiors.update(s)
    return superiors