from src.apps.users.repos import UserRepo


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    def list(self) -> dict:
        return self.repo.get_all()
