from unittest.mock import patch, Mock, MagicMock

from src.api.rbac.repos.user_repo import UserRepo
from src.api.user.repos.userprofile_repo import UserProfileRepo
from src.api.user.services.me_service import MeService


class TestMeService:
    @patch("src.core.storage.provider.resources.s3_session")
    async def test_home_page(self, mock_session: MagicMock, test_db):
        mock_session.client.return_value = Mock()

        await UserRepo(test_db).batch_create(
            [{"id": 1, "name": "csdfsdf", "email": "jcsdfd@ds.com", "password": "occwidfs"}]
        )

        await UserProfileRepo(test_db).batch_create([{"id": 1, "avatar": "aaa.png"}])

        resp_dict = await MeService.home_page(1, test_db)

        assert resp_dict["user_id"] == 1
        assert resp_dict["avatar"]
