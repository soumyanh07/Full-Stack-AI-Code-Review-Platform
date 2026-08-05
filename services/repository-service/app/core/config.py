from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    HOST: str
    PORT: int

    DATABASE_URL: str

    AUTH_SERVICE: str

    GITHUB_TOKEN: str

    REPOSITORY_STORAGE: str = "./repositories"



    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()