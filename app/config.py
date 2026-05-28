from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./todo.db"
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    APP_ENV: str = "development"

    @field_validator("DATABASE_URL")
    @classmethod
    def format_database_url(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
