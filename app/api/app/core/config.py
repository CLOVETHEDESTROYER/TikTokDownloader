import os
import json
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Settings(BaseSettings):
    # API settings
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "your-secret-key")
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "CHANGEME_IN_PRODUCTION!")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # API Security settings
    API_KEY_HEADER_NAME: str = os.getenv("API_KEY_HEADER_NAME", "X-API-Key")
    WEBSITE_API_KEY: str = os.getenv("WEBSITE_API_KEY", "your-website-key")
    REQUIRE_API_KEY: bool = os.getenv(
        "REQUIRE_API_KEY", "true").lower() in ("true", "1", "yes")

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

    # Helper method to parse environment variables that should be lists
    def _parse_list_env(self, env_name: str, default_value: str) -> List[str]:
        value = os.getenv(env_name, default_value)

        # If empty, return empty list
        if not value:
            return []

        # Try to parse as JSON if it starts and ends with brackets
        if value.startswith("[") and value.endswith("]"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass

        # Fall back to comma-separated string
        return [item.strip() for item in value.split(",") if item.strip()]

    # Define properties for all list-type environment variables
    @property
    def CORS_ALLOW_METHODS(self) -> List[str]:
        return self._parse_list_env("CORS_ALLOW_METHODS", "GET,POST,OPTIONS")

    @property
    def CORS_ALLOW_HEADERS(self) -> List[str]:
        return self._parse_list_env(
            "CORS_ALLOW_HEADERS",
            "Content-Type,Authorization,X-Request-ID,X-API-Key,Accept,Origin,Cache-Control"
        )

    @property
    def CORS_EXPOSE_HEADERS(self) -> List[str]:
        return self._parse_list_env("CORS_EXPOSE_HEADERS", "X-Request-ID")

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

        # For production, ensure the DigitalOcean domain is allowed
        if self.ENV == "production":
            origins.append("https://tiksave-7txrl.ondigitalocean.app")
            # Add wildcard for all subdomains on digitalocean.app
            origins.append("https://*.ondigitalocean.app")
            # Add wildcard for custom domains if applicable
            origins.append("https://tiktokwatermarkremover.com")
            origins.append("https://www.tiktokwatermarkremover.com")

        # Remove duplicates and empty strings
        return list(set(origin for origin in origins if origin))

    # Download settings
    DOWNLOAD_FOLDER: str = os.getenv("DOWNLOAD_FOLDER", "downloads")
    LOG_FOLDER: str = os.getenv("LOG_FOLDER", "logs")
    MAX_DOWNLOADS: int = int(os.getenv("MAX_DOWNLOADS", "10"))
    MAX_CONCURRENT_DOWNLOADS: int = int(
        os.getenv("MAX_CONCURRENT_DOWNLOADS", "5"))
    DOWNLOAD_EXPIRY_MINUTES: int = int(os.getenv("DOWNLOAD_EXPIRY_MINUTES", "60"))

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

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Monitoring
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "false").lower() == "true"

    @validator("API_SECRET_KEY", "JWT_SECRET_KEY")
    def validate_secrets(cls, v, values, **kwargs):
        """Validate that secrets are not default in production."""
        env = values.get("ENV")
        if env == "production" and v == "CHANGEME_IN_PRODUCTION!":
            raise ValueError(
                "Secret keys must be changed in production environment")
        return v

    @validator("WEBSITE_API_KEY", "ADMIN_API_KEY")
    def validate_api_keys_in_production(cls, v, values):
        """Validate that API keys are set in production."""
        env = values.get("ENV")
        if env == "production" and values.get("REQUIRE_API_KEY") and not v:
            raise ValueError("API keys must be set in production environment")
        return v

    # Redis (if needed)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    @property
    def CORS_MAX_AGE(self) -> int:
        return int(os.getenv("CORS_MAX_AGE", "3600"))

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings object
settings = Settings()
