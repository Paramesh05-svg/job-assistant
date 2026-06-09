"""
logger.py

Centralized logging configuration for Job Assistant V2.
All modules should import get_logger() from this file.
"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


# --------------------------------------------------
# LOG DIRECTORY
# --------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


# --------------------------------------------------
# LOGGER CONFIGURATION
# --------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.

    Example:
        from src.utils.logger import get_logger

        logger = get_logger(__name__)

        logger.info("Application started")
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # --------------------------------------------------
    # CONSOLE HANDLER
    # --------------------------------------------------

    console_handler = logging.StreamHandler()

    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler.setFormatter(console_formatter)

    # --------------------------------------------------
    # FILE HANDLER
    # --------------------------------------------------

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )

    file_handler.setFormatter(file_formatter)

    # --------------------------------------------------
    # ADD HANDLERS
    # --------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    logger = get_logger(__name__)

    logger.info("Logger initialized successfully")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
