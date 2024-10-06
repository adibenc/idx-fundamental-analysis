import logging

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


# Function to redirect standard logging to Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the log message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
