import secrets
import string

alphabet = string.ascii_letters + string.digits


def generate_verification_code(length: int) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(length))
