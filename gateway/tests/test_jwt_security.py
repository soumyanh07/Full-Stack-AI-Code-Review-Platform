from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.core.config import Settings, settings
from app.security.jwt import create_access_token, verify_access_token


def test_gateway_verifies_auth_service_compatible_hs256_token():
    token = jwt.encode(
        {
            "sub": "user-123",
            "email": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    assert verify_access_token(token)["sub"] == "user-123"


@pytest.mark.parametrize(
    "token",
    [
        "",
        "not-a-jwt",
    ],
)
def test_gateway_rejects_malformed_or_empty_tokens(token):
    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(token)

    assert exc_info.value.status_code == 401


def test_gateway_rejects_expired_or_missing_claim_tokens():
    expired = jwt.encode(
        {"sub": "user-123", "exp": 0},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    missing_subject = jwt.encode(
        {
            "email": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    for token in (expired, missing_subject):
        with pytest.raises(HTTPException) as exc_info:
            verify_access_token(token)
        assert exc_info.value.status_code == 401


def test_gateway_rejects_tampered_and_wrong_secret_tokens(monkeypatch):
    token = create_access_token({"sub": "user-123"})
    header, payload, signature = token.split(".")
    tampered_signature = ("A" if signature[0] != "A" else "B") + signature[1:]
    tampered = f"{header}.{payload}.{tampered_signature}"

    with pytest.raises(HTTPException):
        verify_access_token(tampered)

    monkeypatch.setattr(settings, "SECRET_KEY", "different-secret-key-for-tests")
    with pytest.raises(HTTPException):
        verify_access_token(token)


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
    monkeypatch.setenv("SECRET_KEY", "b" * 40)
    monkeypatch.setenv("ALGORITHM", "HS256")

    configured = Settings(_env_file=None)

    assert configured.ENVIRONMENT == "production"
    assert configured.SECRET_KEY == "b" * 40
    assert configured.ALGORITHM == "HS256"
