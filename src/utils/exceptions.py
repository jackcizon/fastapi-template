# pragma: no cover


class BizException(Exception):
    code: int = 400
    message: str = "biz error"

    def __init__(self, message: str = ""):
        self.message = message


class AuthError(BizException):
    code = 401
    message = "auth failed"


class NotFoundError(BizException):
    code = 404
    message = "not found"
