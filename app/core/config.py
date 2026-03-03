"""
Application Configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    SYSTEM_EMAIL: str
    
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 2
    
    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    SMTP_FROM_NAME: str
    SMTP_SUPPORT_EMAIL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,https://bantuevents.com,https://mainapi.bantuevents.com"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Security
    SECRET_KEY: str
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Parse allowed hosts from comma-separated string"""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_IMAGE_TYPES: str = "jpg,jpeg,png,gif,webp"
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        """Parse allowed image types from comma-separated string"""
        return [ext.strip() for ext in self.ALLOWED_IMAGE_TYPES.split(",")]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5

    # Email Settings
    EMAIL_USE_SSL: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"

    # URLs
    FRONTEND_BASE_URL: str
    BASE_URL: str

    # Testing
    TEST_DATABASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()