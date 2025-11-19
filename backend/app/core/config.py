import os
from typing import List
from pydantic import field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden via environment variables or .env file.
    For production, ensure SECRET_KEY is set via environment variable.
    """
    # Environment
    ENVIRONMENT: str = "development"

    # Security settings
    SECRET_KEY: str = "secret-key-change-in-production-MUST-BE-64-CHARS-MINIMUM-PLEASE-CHANGE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Password validation settings
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    # Rate limiting settings
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_AUTH_PER_MINUTE: int = 5

    # Database settings
    DATABASE_URL: str = "sqlite:///./backend.db"
    AUTO_CREATE_TABLES: bool = False

    # CORS settings - MUST be explicitly set in production
    CORS_ORIGINS: List[str] = []

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # API settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Task Management API"
    PROJECT_VERSION: str = "1.0.0"

    # Database connection pool settings (for production databases)
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True

    # Email settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Task Management"
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_EXPIRE_HOURS: int = 1

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    CACHE_TTL_SECONDS: int = 300

    # Frontend URL for email links
    FRONTEND_URL: str = "http://localhost:5173"

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info: ValidationInfo) -> str:
        """Validate SECRET_KEY length in production."""
        environment = info.data.get("ENVIRONMENT", "development")
        if environment == "production":
            if not v or len(v) < 64:
                raise ValueError(
                    "SECRET_KEY must be at least 64 characters in production. "
                    "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(64))'"
                )
            if v == "secret-key-change-in-production-MUST-BE-64-CHARS-MINIMUM-PLEASE-CHANGE":
                raise ValueError(
                    "SECRET_KEY must be changed from default in production. "
                    "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(64))'"
                )
        return v

    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: List[str], info: ValidationInfo) -> List[str]:
        """Ensure CORS origins are explicitly set in production."""
        environment = info.data.get("ENVIRONMENT", "development")
        if environment == "production" and not v:
            raise ValueError(
                "CORS_ORIGINS must be explicitly set in production. "
                "Wildcards are not allowed for security reasons."
            )
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()