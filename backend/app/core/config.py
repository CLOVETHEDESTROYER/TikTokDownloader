import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Settings(BaseSettings):
    # API settings
    API_SECRET_KEY: str = os.getenv(
        "API_SECRET_KEY", "CHANGEME_IN_PRODUCTION!")
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "CHANGEME_IN_PRODUCTION!")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "4"))

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ADDITIONAL_ALLOWED_ORIGINS: str = os.getenv(
        "ADDITIONAL_ALLOWED_ORIGINS", "")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv(
        "CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    CORS_ALLOW_METHODS: List[str] = os.getenv(
        "CORS_ALLOW_METHODS", "GET,POST,OPTIONS").split(",")
    CORS_ALLOW_HEADERS: List[str] = os.getenv(
        "CORS_ALLOW_HEADERS",
        "Content-Type,Authorization,X-Request-ID,X-API-Key,Accept,Origin,Cache-Control"
    ).split(",")
    CORS_EXPOSE_HEADERS: List[str] = os.getenv(
        "CORS_EXPOSE_HEADERS", "X-Request-ID").split(",")
    CORS_MAX_AGE: int = int(os.getenv("CORS_MAX_AGE", "3600"))

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Get list of allowed origins for CORS."""
        origins = [self.FRONTEND_URL]

        # Always allow localhost in development
        if self.ENV == "development":
            origins.extend([
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8000",
            ])

        # Add additional origins if specified
        if self.ADDITIONAL_ALLOWED_ORIGINS:
            origins.extend(
                [o.strip() for o in self.ADDITIONAL_ALLOWED_ORIGINS.split(",") if o.strip()])

        # Remove duplicates and empty strings
        return list(set(origin for origin in origins if origin))

    # Download settings
    DOWNLOAD_FOLDER: str = os.getenv("DOWNLOAD_FOLDER", "downloads")
    MAX_DOWNLOADS: int = int(os.getenv("MAX_DOWNLOADS", "10"))
    MAX_CONCURRENT_DOWNLOADS: int = int(
        os.getenv("MAX_CONCURRENT_DOWNLOADS", "5"))
    DOWNLOAD_EXPIRY_HOURS: int = int(os.getenv("DOWNLOAD_EXPIRY_HOURS", "24"))

    # Security settings
    VERIFY_SSL: bool = os.getenv(
        "VERIFY_SSL", "false").lower() in ("true", "1", "yes")
    ADMIN_API_KEY: Optional[str] = os.getenv("ADMIN_API_KEY")

    # Instagram settings
    INSTAGRAM_COOKIES_FILE: str = os.getenv(
        "INSTAGRAM_COOKIES_FILE", "config/instagram_cookies.txt")
    INSTAGRAM_MAX_RETRIES: int = int(os.getenv("INSTAGRAM_MAX_RETRIES", "3"))
    INSTAGRAM_TIMEOUT: int = int(os.getenv("INSTAGRAM_TIMEOUT", "30"))
    CONFIG_DIR: str = os.getenv("CONFIG_DIR", "config")

    @validator("API_SECRET_KEY", "JWT_SECRET_KEY")
    def validate_secrets(cls, v, values, **kwargs):
        """Validate that secrets are not default in production."""
        env = values.get("ENV")
        if env == "production" and v == "CHANGEME_IN_PRODUCTION!":
            raise ValueError(
                "Secret keys must be changed in production environment")
        return v

    # Redis (if needed)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings object
settings = Settings()
