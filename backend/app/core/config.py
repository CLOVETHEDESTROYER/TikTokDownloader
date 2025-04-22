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

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Get list of allowed origins for CORS."""
        origins = [self.FRONTEND_URL]

        # Always allow localhost in development
        if self.ENV == "development":
            origins.extend([
                "http://localhost:3000",
                "http://localhost:8000",
            ])

        # Add additional origins if specified
        if self.ADDITIONAL_ALLOWED_ORIGINS:
            origins.extend(
                [o.strip() for o in self.ADDITIONAL_ALLOWED_ORIGINS.split(",") if o.strip()])

        # Remove duplicates
        return list(set(origins))

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
