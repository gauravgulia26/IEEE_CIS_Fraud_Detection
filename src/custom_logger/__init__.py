import logging
import os
from datetime import datetime
from pathlib import Path


def get_logger(name: str, log_dir_path: Path) -> logging.Logger:
    """
    Create and return a configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    LOG_DIR = log_dir_path
    os.makedirs(LOG_DIR, exist_ok=True)

    # Log file name with timestamp
    LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

    # Avoid duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_PATH)
        console_handler = logging.StreamHandler()

        # Formatter
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
