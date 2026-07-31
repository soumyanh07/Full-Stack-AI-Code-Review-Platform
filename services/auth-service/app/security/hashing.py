import bcrypt


def _normalize_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return password_bytes


def hash_password(password: str) -> str:
    normalized_password = _normalize_password(password)
    hashed_bytes = bcrypt.hashpw(normalized_password, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    normalized_password = _normalize_password(password)
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(normalized_password, hashed_password_bytes)