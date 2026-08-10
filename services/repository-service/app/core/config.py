from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.
    """

    # ==========================
    # Application
    # ==========================
    APP_NAME: str = "Repository Service"
    API_VERSION: str = "v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8002

    DEBUG: bool = True

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:1234@localhost:5432/ai_code_review"
    )

    # ==========================
    # JWT
    # ==========================
    SECRET_KEY: str = (
        "704ebd3cd433e4e48169e774ffe2ad8114766a38d346978600cf8c1c77984943"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==========================
    # GitHub
    # ==========================
    GITHUB_TOKEN: str
    REPOSITORY_STORAGE: str = "./storage/repositories"

    # ==========================
    # Ollama
    # ==========================
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5-coder:7b"

    # ==========================
    # Qdrant
    # ==========================
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "repository_chunks"

    # ==========================
    # Embedding Model
    # ==========================
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384

    # ==========================
    # Redis
    # ==========================
    REDIS_URL: str = "redis://localhost:6379/0"

    # ==========================
    # Pydantic Settings
    # ==========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """
    return Settings()


settings = get_settings()