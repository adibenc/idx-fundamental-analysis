# logger_config.py
from loguru import logger

# Configure the logger to write to a log file
logger.add(
    "logs/app.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 MB",  # Rotate after the log file reaches 1 MB
    retention="10 days",  # Keep rotated files for 10 days
    compression="zip",  # Compress rotated files
)

# Export the logger for use in other modules
__all__ = ["logger"]
