from unittest.mock import patch, Mock, MagicMock

import pytest

from src.api.user.schemas.avatar_schema import AvatarUploadRequest, AvatarUploadCallbackRequest
from src.api.user.services.avatar_service import AvatarService
from src.core.exceptions.auth import AuthError


class TestAvatarService:
    filename = "aaa.png"
    wrong_filename = "aaa.txt"
    key = "user/1/avatar/aaa.png"
    invalid_key = "invalid/1/avatar/aaa.png"

    @patch("src.core.storage.provider.resources.s3_session")
    async def test_upload_success(self, mock_s3_session: Mock):
        mock_s3_session.client.return_value = Mock()

        req = AvatarUploadRequest(filename=self.filename)
        resp_dict = await AvatarService.upload(req, 1)

        assert resp_dict["avatar_put_url"]
        assert resp_dict["key"]

    async def test_upload_failed_invalid_file_type(self):
        req = AvatarUploadRequest(filename=self.wrong_filename)
        with pytest.raises(AuthError):
            await AvatarService.upload(req, 1)

    @patch("src.core.storage.provider.resources.s3_session")
    async def test_upload_callback_success(self, mock_s3_session: MagicMock, test_db):
        mock_s3_session.client.return_value = MagicMock()

        req = AvatarUploadCallbackRequest(key=self.key)
        await AvatarService.upload_callback(req, 1, test_db)

    @patch("src.core.storage.provider.resources.s3_session")
    async def upload_callback_failed_invalid_key(self, mock_s3_session: MagicMock, test_db):
        mock_s3_session.client.return_value = MagicMock()

        req = AvatarUploadCallbackRequest(key=self.invalid_key)
        await AvatarService.upload_callback(req, 1, test_db)
