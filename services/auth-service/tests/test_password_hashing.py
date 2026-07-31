from app.security.hashing import hash_password, verify_password


def test_hash_and_verify_long_password():
    password = "a" * 100

    hashed_password = hash_password(password)

    assert hashed_password
    assert verify_password(password, hashed_password) is True
