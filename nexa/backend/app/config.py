"""Application configuration for the Nexa backend."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, HttpUrl


class Settings(BaseSettings):
    """Runtime application settings."""

    environment: str = Field("development", env="NEXA_ENV")
    version: str = Field("0.1.0", env="NEXA_VERSION")

    # CORS
    cors_allowed_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        env="NEXA_CORS_ALLOWED_ORIGINS",
    )

    # API Keys
    openweather_api_key: str = Field("", env="OPENWEATHER_API_KEY")
    news_api_key: str = Field("", env="NEWS_API_KEY")
    spotify_client_id: str = Field("", env="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = Field("", env="SPOTIFY_CLIENT_SECRET")

    # External services
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    database_url: str = Field("sqlite+aiosqlite:///./nexa.db", env="DATABASE_URL")
    websocket_origin: HttpUrl | None = Field(None, env="NEXA_WEBSOCKET_ORIGIN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        arbitrary_types_allowed = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings with caching."""
    return Settings()

