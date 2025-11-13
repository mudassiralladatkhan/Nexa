"""
Nexa Backend Configuration
Manages all application settings, API keys, and environment variables
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Nexa Voice Assistant"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Database
    database_url: str = Field(default="sqlite:///./nexa.db", env="DATABASE_URL")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Voice Settings
    wake_words: List[str] = Field(
        default=["nexa", "hey nexa", "ok nexa"],
        env="WAKE_WORDS"
    )
    voice_timeout: int = Field(default=5, env="VOICE_TIMEOUT")
    speech_language: str = Field(default="en-US", env="SPEECH_LANGUAGE")
    
    # API Keys - Weather
    openweather_api_key: Optional[str] = Field(default=None, env="OPENWEATHER_API_KEY")
    weatherapi_key: Optional[str] = Field(default=None, env="WEATHERAPI_KEY")
    
    # API Keys - News
    newsapi_key: Optional[str] = Field(default=None, env="NEWSAPI_KEY")
    
    # API Keys - Music
    spotify_client_id: Optional[str] = Field(default=None, env="SPOTIFY_CLIENT_ID")
    spotify_client_secret: Optional[str] = Field(default=None, env="SPOTIFY_CLIENT_SECRET")
    
    # API Keys - AI/LLM
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    
    # API Keys - Maps/Location
    google_maps_api_key: Optional[str] = Field(default=None, env="GOOGLE_MAPS_API_KEY")
    
    # Redis (for caching and background tasks)
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # Background Services
    enable_background_listening: bool = Field(default=True, env="ENABLE_BACKGROUND_LISTENING")
    background_service_interval: int = Field(default=1, env="BACKGROUND_SERVICE_INTERVAL")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Performance
    max_concurrent_requests: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")
    
    # File Storage
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings():
    """Reload settings from environment"""
    global _settings
    _settings = None
    return get_settings()


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"


class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    log_level: str = "WARNING"
    

class TestingSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    database_url: str = "sqlite:///./test_nexa.db"
    log_level: str = "DEBUG"


def get_settings_for_env(env: str = None) -> Settings:
    """Get settings for specific environment"""
    env = env or os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Validation helpers
def validate_api_keys(settings: Settings) -> List[str]:
    """Validate that required API keys are present"""
    missing_keys = []
    
    # Check critical API keys
    if not settings.openweather_api_key and not settings.weatherapi_key:
        missing_keys.append("Weather API key (OPENWEATHER_API_KEY or WEATHERAPI_KEY)")
    
    if not settings.newsapi_key:
        missing_keys.append("News API key (NEWSAPI_KEY)")
    
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        missing_keys.append("Spotify API credentials (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)")
    
    return missing_keys


def get_feature_flags(settings: Settings) -> dict:
    """Get feature availability based on API keys"""
    return {
        "weather": bool(settings.openweather_api_key or settings.weatherapi_key),
        "news": bool(settings.newsapi_key),
        "music": bool(settings.spotify_client_id and settings.spotify_client_secret),
        "ai_chat": bool(settings.openai_api_key or settings.google_api_key),
        "maps": bool(settings.google_maps_api_key),
        "background_listening": settings.enable_background_listening,
    }
