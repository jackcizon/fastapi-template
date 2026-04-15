from src.api.auth.schemas.email_schema import EmailVerificationRequest
from src.api.auth.services.email_verification_service import EmailVerificationService


class TestEmailVerificationService:
    async def test_verify_success(self, test_cache):
        # params = [{"name": "test", "email": "email@test.com", "password": "123456789"}]
        # stat = Insert(User)
        # await test_db.execute(stat, params)
        # await test_db.flush()

        req = EmailVerificationRequest(email="email@test.com")
        resp = await EmailVerificationService.verify(req, test_cache)
        # await EmailVerificationService.notify()  dev does not need to test, a little complex
        assert len(resp["verification_code"]) == 9

    # async def test_verify_failed(self, test_cache):
    #     # user = User(name="test", email="email@test.com", password="12234567")
    #     # test_db.add(user)
    #     # await test_db.flush()
    #
    #     req = EmailVerificationRequest(email="11111111@qq.com")
    #
    #     with pytest.raises(AuthError):
    #         await EmailVerificationService.verify(req, test_cache)
