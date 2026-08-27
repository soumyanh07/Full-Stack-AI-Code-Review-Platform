from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    HOST: str
    PORT: int

    DATABASE_URL: str

    AUTH_SERVICE: str

    GITHUB_TOKEN: str

    # GitHub App configuration
    GITHUB_APP_ID: int
    GITHUB_APP_PRIVATE_KEY_PATH: str
    GITHUB_APP_INSTALLATION_ID: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
