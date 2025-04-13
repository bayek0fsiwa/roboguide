import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = BASE_DIR = pathlib.Path(__file__).parent.parent.parent
ENV_DIR = BASE_DIR / ".env"


class Settings(BaseSettings):
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    DATABASE_URL: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: int
    PORT: int
    GEMINI_KEY: str = ""
    GEMINI_URL: str = ""
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""
    COGNITO_CLIENT_NAME: str = ""
    COGNITO_CLIENT_ID: str = ""
    COGNITO_CLIENT_SECRET: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
