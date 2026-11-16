from datetime import datetime, timedelta, timezone

import jwt
import pytest
from pydantic import ValidationError

from app.core.config import Settings, settings
from app.security import jwt as jwt_module
from app.security.jwt import create_access_token, verify_token


@pytest.mark.parametrize(
    "payload",
    [
        {"sub": "user-123"},
        {"sub": "user-456", "role": "admin"},
    ],
)
def test_create_and_verify_valid_token(payload):
    token = create_access_token(payload)
    decoded = verify_token(token)

    assert decoded is not None
    assert decoded["sub"] == payload["sub"]
    assert decoded["exp"]


def test_verify_rejects_missing_claims():
    token = jwt.encode(
        {
            "email": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    assert verify_token(token) is None


def test_verify_rejects_expired_token():
    expired = create_access_token({"sub": "user-123"}, expires_delta=timedelta(minutes=-5))
    assert verify_token(expired) is None


def test_verify_rejects_tampered_token():
    token = create_access_token({"sub": "user-123"})
    header, payload, signature = token.split(".")
    tampered_signature = ("A" if signature[0] != "A" else "B") + signature[1:]
    tampered = f"{header}.{payload}.{tampered_signature}"
    assert verify_token(tampered) is None


def test_verify_rejects_wrong_secret():
    token = create_access_token({"sub": "user-123"})
    original_secret = jwt_module.SECRET_KEY
    jwt_module.SECRET_KEY = "different-secret-key-for-tests-should-fail"
    try:
        assert verify_token(token) is None
    finally:
        jwt_module.SECRET_KEY = original_secret


def test_verify_rejects_empty_token():
    assert verify_token("") is None
    assert verify_token("   ") is None


@pytest.mark.parametrize(
    "secret",
    [
        "",
        "secret-key-please-change-this-before-production-12345",
        "short",
        "x" * 31,
        "dev-secret-key-change-me-in-production-32+",
        "replace_with_at_least_32_chars_random_secret",
    ],
)
def test_production_settings_reject_weak_or_placeholder_secrets(secret):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, ENVIRONMENT="production", SECRET_KEY=secret)


def test_production_settings_reject_default_secret():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, ENVIRONMENT="production")


def test_production_settings_accept_32_character_secret():
    configured = Settings(
        _env_file=None,
        ENVIRONMENT="production",
        SECRET_KEY="x" * 32,
    )

    assert configured.SECRET_KEY == "x" * 32


def test_settings_accept_environment_overrides(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "a" * 40)
    monkeypatch.setenv("ALGORITHM", "HS256")

    configured = Settings(_env_file=None)

    assert configured.ENVIRONMENT == "production"
    assert configured.SECRET_KEY == "a" * 40
    assert configured.ALGORITHM == "HS256"
