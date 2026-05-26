import logging

from datetime import datetime
from pathlib import Path
from src.configs.paths import PROJ_ROOT

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):

        log_color = self.COLORS.get(record.levelno, Fore.WHITE)

        formatted_message = super().format(record)

        return f"{log_color}{formatted_message}{Style.RESET_ALL}"


def get_logger(
    name: str,
    log_dir_path: Path,
) -> logging.Logger:
    """
    Create and return configured logger
    with colored console output
    """

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    logger.propagate = False
    log_dir_path_full = PROJ_ROOT / log_dir_path
    log_dir_path_full.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

    log_path = log_dir_path_full / log_file

    if not logger.handlers:

        # Console Handler
        console_handler = logging.StreamHandler()

        console_formatter = ColoredFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        console_handler.setFormatter(console_formatter)

        # File Handler
        file_handler = logging.FileHandler(log_path)

        file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)

        logger.addHandler(file_handler)

    return logger
