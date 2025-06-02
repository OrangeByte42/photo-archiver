import os
import shutil
import logging
from typing import Dict, Any, List, Tuple

import yaml

from src.utils.scripts import assert_abs_paths_exist
from src.config.loader import load_config
from src.config.logging_config import setup_logging, clear_logging_handlers


_FLATTEN_JPGS_CONFIG_FILE = "config/flatten_jpgs_config.yaml"

def _build_prefix(root_dir: str, dirpath: str) -> str:
    """
    Given the root directory and the directory of a file, build the prefix string
    composed of the root folder name plus any subfolder names, separated by hyphens.
    """
    relpath: str = os.path.relpath(dirpath, root_dir)
    parts: List[str] = [] if relpath == "." else relpath.split(os.sep)
    return '-'.join(parts) if parts else ""

def flatten_jpgs_main(config_file_path: str = _FLATTEN_JPGS_CONFIG_FILE) -> None:
    """
    Main function to flatten JPG files based on a configuration file.
    """
    # Load configuration from YAML file
    config: Dict[str, Any] = load_config(config_file_path)
    # Extract configuration parameters
    input_jpg_dir_abs_path: str = config["input_jpg_dir_abs_path"]
    output_jpg_dir_abs_path: str = config["output_jpg_dir_abs_path"]
    jpg_exts: List[str] = config["jpg_exts"]
    number_of_digits: int = config["number_of_digits"]

    # Configure logging
    log_file_abs_path: str = config["log_file_abs_path"]
    setup_logging(log_to_file=True, log_file_abs_path=log_file_abs_path)

    # Check if the provided paths exist
    assert_abs_paths_exist(
        [input_jpg_dir_abs_path, output_jpg_dir_abs_path]
    )

    # Main logic
    # 1. collect JPG files from the input directory
    logging.info("Collecting JPG files from the input directory...")
    jpg_files: List[Tuple[Any, str]] = []
    for dirpath, _, filenames in os.walk(input_jpg_dir_abs_path):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in jpg_exts:
                jpg_files.append((dirpath, filename))
    # 2. Flatten JPG files into the output directory
    jpg_rename_counters: Dict[str, int] = {}
    for dirpath, filename in jpg_files:
        old_path = os.path.join(dirpath, filename)
        prefix = _build_prefix(input_jpg_dir_abs_path, dirpath)
        # Initialize counter if needed
        jpg_rename_counters.setdefault(prefix, 0)
        jpg_rename_counters[prefix] += 1
        seq = jpg_rename_counters[prefix]
        # Format new filename with prefix and sequence number
        ext = os.path.splitext(filename)[1].lower()
        new_jpg_name = f"{prefix}-{seq:0{number_of_digits}d}{ext}" if prefix else f"{seq:0{number_of_digits}d}{ext}"
        new_path = os.path.join(output_jpg_dir_abs_path, new_jpg_name)
        # If the new path already exists, skip it
        try:
            shutil.move(old_path, new_path)
            logging.info(f"Moved: {old_path} -> {new_path}")
        except Exception as e:
            logging.error(f"Failed to move {old_path} to {new_path}: {e}")

    logging.info(f"All JPG files have been moved and renamed successfully.")

    # Clear logging handlers to prevent duplicate logs in future runs
    clear_logging_handlers()

if __name__ == "__main__":
    # Run the main function with the default configuration file path
    flatten_jpgs_main(config_file_path=_FLATTEN_JPGS_CONFIG_FILE)







