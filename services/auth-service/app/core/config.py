from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Code Review Auth Service"
    API_VERSION: str = "v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8001

    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./auth.db"

    SECRET_KEY: str = "THIS_IS_A_LONG_RANDOM_SECRET_KEY_CHANGE_ME"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()