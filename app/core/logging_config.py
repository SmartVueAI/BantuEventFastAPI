"""
Logging Configuration
"""
from loguru import logger
import sys
from pathlib import Path


def setup_logging():
    """Configure application logging with loguru"""
    
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # Create logs directory if it doesn't exist
    # Path("logs").mkdir(exist_ok=True)

    log_dir = Path("/app/logs")
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        # File handler with rotation
        logger.add(
            str(log_dir / "app_{time:YYYY-MM-DD}.log"),
                rotation="00:00",  # Rotate at midnight
                retention="30 days",  # Keep logs for 30 days
                level="INFO",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
                serialize=True,  # JSON format
                backtrace=True,
            diagnose=True
        )

        # Error file handler
        logger.add(
            str(log_dir / "error_{time:YYYY-MM-DD}.log"),
                rotation="00:00",
                retention="30 days",
                level="ERROR",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
                serialize=True,
                backtrace=True,
            diagnose=True
        )

        logger.info("Logging configured successfully")
    except PermissionError:
        logger.warning("Cannot write to /app/logs, logging to stdout only")

# Sanitize sensitive data from logs
def sanitize_log_data(data: dict) -> dict:
    """Remove sensitive fields from log data"""
    sensitive_fields = [
        "password",
        "hashed_password",
        "token",
        "access_token",
        "refresh_token",
        "verification_token",
        "otp",
        "security_stamp",
    ]
    
    sanitized = data.copy()
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = "***REDACTED***"
    
    return sanitized