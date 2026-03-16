from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password:
    @staticmethod
    def hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    pwd = "123456"
    # wrong
    assert (Password.hash(pwd) == Password.hash(pwd)) is False
    hashed_pwd = Password.hash(pwd)
    # right
    assert (Password.verify(pwd, hashed_pwd)) is True
