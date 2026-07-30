"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    allowed_origins: str = "http://localhost:5500,http://127.0.0.1:5500,https://sayam.eu.org"
    resend_api_key: str = ""
    resend_from_email: str = ""
    notification_email: str = "contact@sayam.eu.org"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
