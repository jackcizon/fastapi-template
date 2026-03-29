from src.utils.helpers import get_superior_roles


class TestGetSuperiorRoles:
    def test_get_superior_roles(self):
        map_ = {
            # role: [child1, child2] or []
            "user": [],
            "staff": ["user"],
            "finance": ["staff"],
            "cto": ["staff"],
            "ceo": ["finance", "cto"],
            "chairman": ["ceo"],
        }

        ret1 = get_superior_roles("user", map_)
        assert "user" in ret1
        assert {"user"}.issubset(ret1)

        ret2 = get_superior_roles("chairman", map_)
        assert "user" not in ret2
        assert {"chairman"} == ret2
