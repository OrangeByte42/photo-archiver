import logging
import os
from typing import Any


def setup_logging(log_level: Any=logging.INFO, log_to_file: bool=False, log_file_abs_path: str = None) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=os.path.abspath(log_file_abs_path) if log_to_file and log_file_abs_path else None,
        filemode='a',
    )

def clear_logging_handlers() -> None:
    """
    Clear all logging handlers to prevent duplicate logs.
    """
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)



