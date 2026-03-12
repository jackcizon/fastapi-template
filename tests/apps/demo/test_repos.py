from src.apps.demo.repos import DemoRepo


class TestDemoRepo:
    def test_create_demo(self, db):
        repo = DemoRepo(db=db)
        demo = repo.create_demo(name="demo1")
        assert demo.id is not None

    def test_get_login_demo(self, db):
        repo = DemoRepo(db=db)

        demo = repo.create_demo(name="demo2")

        result = repo.get_demo_by_id(demo.id)

        assert result is not None
        assert result.id == demo.id
