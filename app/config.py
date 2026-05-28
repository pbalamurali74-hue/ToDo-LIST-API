import os
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./todo.db"
    JWT_ACCESS_SECRET: str = "fallback-access-secret-key-change-in-prod"
    JWT_REFRESH_SECRET: str = "fallback-refresh-secret-key-change-in-prod"
    APP_ENV: str = "development"

    @field_validator("DATABASE_URL")
    @classmethod
    def format_database_url(cls, v: str) -> str:
        # Vercel environment filesystem is read-only except for /tmp
        if os.getenv("VERCEL") == "1" and v == "sqlite:///./todo.db":
            return "sqlite:////tmp/todo.db"

        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
