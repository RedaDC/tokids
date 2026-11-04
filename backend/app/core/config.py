"""
TeeDesign AI — Application Configuration
"""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_ENV: Literal["development", "production", "test"] = "development"
    APP_SECRET_KEY: str = "dev-secret-key-change-in-production"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "TeeDesign AI"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://teedesign:teedesign_pass@localhost:5432/teedesign_db"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://teedesign:teedesign_pass@localhost:5432/teedesign_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # JWT
    JWT_SECRET_KEY: str = "dev-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Default Admin
    ADMIN_EMAIL: str = "admin@teedesign.ai"
    ADMIN_PASSWORD: str = "TeeDesign2024!"
    ADMIN_USERNAME: str = "admin"

    # LLM
    LLM_PROVIDER: Literal["openai", "anthropic", "google", "stub"] = "stub"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 4096
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-1.5-pro"

    # Image Generation
    IMAGE_PROVIDER: Literal["openai", "replicate", "stub"] = "stub"
    DALLE_MODEL: str = "dall-e-3"
    DALLE_SIZE: str = "1024x1024"
    DALLE_QUALITY: str = "hd"
    REPLICATE_API_KEY: str = ""
    REPLICATE_MODEL: str = "black-forest-labs/flux-schnell"

    # Image Processing
    EXPORT_WIDTH: int = 5000
    EXPORT_HEIGHT: int = 5500
    PREVIEW_WIDTH: int = 600
    PREVIEW_HEIGHT: int = 600
    MIN_QUALITY_SCORE: float = 70.0

    # Storage paths
    STORAGE_PATH: str = "./assets"
    MASTER_FILES_PATH: str = "./assets/generated"
    APPROVED_FILES_PATH: str = "./assets/approved"
    PREVIEWS_PATH: str = "./assets/previews"
    EXPORTS_PATH: str = "./assets/exports"

    # Langfuse
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    # Cost Controls
    MAX_DAILY_SPEND_USD: float = 50.00
    MAX_MONTHLY_SPEND_USD: float = 500.00
    MAX_RETRIES_PER_DESIGN: int = 3
    MAX_WORKFLOW_STEPS: int = 50

    @property
    def is_stub_mode(self) -> bool:
        return self.LLM_PROVIDER == "stub" or not self.OPENAI_API_KEY

    @property
    def cors_origins(self) -> list[str]:
        return [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
        ]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
