import re

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Code Review Auth Service"
    API_VERSION: str = "v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8001
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@postgres:5432/ai_code_review"

    SECRET_KEY: str = "dev-secret-key-change-me-in-production-32+"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str, info: ValidationInfo) -> str:
        cleaned = value.strip()
        environment = str(info.data.get("ENVIRONMENT", "development")).strip().lower()
        if not cleaned:
            raise ValueError("SECRET_KEY must not be empty")
        if len(cleaned) < 16:
            raise ValueError("SECRET_KEY must be at least 16 characters")
        if environment == "production":
            normalized = re.sub(r"[^a-z0-9]", "", cleaned.lower())
            if len(cleaned) < 32:
                raise ValueError("SECRET_KEY must be at least 32 characters in production")
            if any(
                marker in normalized
                for marker in (
                    "secret",
                    "password",
                    "changeme",
                    "changeit",
                    "replace",
                    "placeholder",
                    "example",
                    "your",
                    "default",
                    "devsecret",
                    "developmentsecret",
                    "testsecret",
                    "insecure",
                )
            ):
                raise ValueError("SECRET_KEY must not be a placeholder or default in production")
        return cleaned

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, value: str) -> str:
        algorithm = value.strip()
        if algorithm not in {"HS256"}:
            raise ValueError("Unsupported JWT algorithm. Only HS256 is allowed.")
        return algorithm


settings = Settings()