
import bcrypt


def _normalize_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")

    # bcrypt supports only the first 72 bytes
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    return password_bytes


def hash_password(password: str) -> str:
    password_bytes = _normalize_password(password)
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        password_bytes = _normalize_password(password)
        hashed_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hashed_bytes)

    except Exception:
        return False