import hashlib
import hmac

import pytest
from pydantic import ValidationError


@pytest.fixture
def webhook_module(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("SECRET_KEY", "repository-test-secret-key")
    monkeypatch.setenv("GITHUB_TOKEN", "repository-test-token")
    monkeypatch.delenv("GITHUB_WEBHOOK_SECRET", raising=False)

    from app.api.v1 import webhook

    return webhook


def test_verify_signature_accepts_valid_hmac_sha256(webhook_module, monkeypatch):
    secret = "webhook-test-secret"
    body = b'{"action":"opened"}'
    signature = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
    monkeypatch.setattr(webhook_module.settings, "GITHUB_WEBHOOK_SECRET", secret)

    assert webhook_module._verify_signature(body, signature) is True


def test_verify_signature_rejects_missing_signature(webhook_module, monkeypatch):
    monkeypatch.setattr(
        webhook_module.settings,
        "GITHUB_WEBHOOK_SECRET",
        "webhook-test-secret",
    )

    assert webhook_module._verify_signature(b"payload", None) is False


def test_verify_signature_rejects_invalid_signature(webhook_module, monkeypatch):
    monkeypatch.setattr(
        webhook_module.settings,
        "GITHUB_WEBHOOK_SECRET",
        "webhook-test-secret",
    )

    assert webhook_module._verify_signature(b"payload", "sha256=invalid") is False


def test_empty_webhook_secret_allows_unsigned_development_webhook(
    webhook_module,
    monkeypatch,
):
    monkeypatch.setattr(webhook_module.settings, "ENVIRONMENT", "development")
    monkeypatch.setattr(webhook_module.settings, "GITHUB_WEBHOOK_SECRET", "")

    assert webhook_module._verify_signature(b"payload", None) is True


def test_empty_webhook_secret_rejects_unsigned_production_webhook(
    webhook_module,
    monkeypatch,
):
    monkeypatch.setattr(webhook_module.settings, "ENVIRONMENT", "production")
    monkeypatch.setattr(webhook_module.settings, "GITHUB_WEBHOOK_SECRET", "")

    assert webhook_module._verify_signature(b"payload", None) is False


def test_environment_defaults_to_development(webhook_module, monkeypatch):
    from app.core.config import Settings

    monkeypatch.delenv("ENVIRONMENT", raising=False)
    configured = Settings(
        _env_file=None,
        SECRET_KEY="repository-test-secret-key",
        GITHUB_TOKEN="repository-test-token",
    )

    assert configured.ENVIRONMENT == "development"


@pytest.mark.parametrize("webhook_secret", [None, "   "])
def test_production_settings_reject_missing_or_blank_webhook_secret(
    webhook_module,
    webhook_secret,
    monkeypatch,
):
    from app.core.config import Settings

    monkeypatch.setenv("ENVIRONMENT", "production")
    values = {
        "_env_file": None,
        "SECRET_KEY": "repository-test-secret-key",
        "GITHUB_TOKEN": "repository-test-token",
    }
    if webhook_secret is not None:
        values["GITHUB_WEBHOOK_SECRET"] = webhook_secret

    with pytest.raises(ValidationError, match="GITHUB_WEBHOOK_SECRET"):
        Settings(**values)
