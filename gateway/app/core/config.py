from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.
    """

    # ==========================
    # Application
    # ==========================
    APP_NAME: str = "AI Code Review Gateway"
    API_VERSION: str = "v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DEBUG: bool = True

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:password@localhost:5432/ai_code_review"
    )

    # ==========================
    # JWT
    # ==========================
    SECRET_KEY: str = "change-this-to-a-strong-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==========================
    # Microservices
    # ==========================
    AUTH_SERVICE: str = "http://localhost:8001"
    REPOSITORY_SERVICE: str = "http://localhost:8002"
    REVIEW_SERVICE: str = "http://localhost:8003"
    AI_SERVICE: str = "http://localhost:8004"
    CHAT_SERVICE: str = "http://localhost:8005"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()