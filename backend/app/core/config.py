# ABOUTME: Centralized runtime configuration for API keys, auth, and DB settings.
# ABOUTME: Loads typed environment variables used across backend services.
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    jwt_secret: str = "dev-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    bloomberg_api_key: str = ""
    fmp_api_key: str = ""
    polygon_api_key: str = ""
    alpha_vantage_api_key: str = ""
    yahoo_enabled: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
