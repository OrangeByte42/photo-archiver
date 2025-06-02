import os
import logging
from typing import Set, Tuple, Dict, List, Any
from pprint import pprint

from src.utils.scripts import TOTAL_JPG_CNT, TOTAL_CAMERA_JPG_CNT, UNIQUE_CAMERA_JPG_CNT
from src.utils.scripts import KEPT_RAW_CNT, DELETED_RAW_CNT, FAILED_DELETE_RAW_CNT
from src.utils.scripts import gather_camera_jpg_names
from src.utils.scripts import filter_raw_files_by_jpg_names

from src.config.loader import load_config
from src.config.logging_config import setup_logging, clear_logging_handlers


def filter_raw_by_jpg_main(config_file_path: str = "config/config.yaml"):
    """
    Main function to filter raw files based on JPG names.
    """
    # Load configuration from YAML file
    config: Dict[str, Any] = load_config(config_file_path)
    # Extract configuration parameters
    jpg_dir_abs_path: str = config['jpg_dir_abs_path']
    raw_dir_abs_path: str = config['raw_dir_abs_path']
    jpg_exts: List[str] = config['jpg_exts']
    raw_exts: List[str] = config['raw_exts']
    camera_prefixes: List[str] = config['camera_prefixes']

    # Configure logging
    log_file_abs_path: str = config['log_file_abs_path']
    setup_logging(log_to_file=True, log_file_abs_path=log_file_abs_path)

    # Main logic
    # 1. Gather JPG names from the specified directory
    logging.info("Gathering JPG file names...")
    camera_jpg_names, detailed_info = gather_camera_jpg_names(
        jpg_dir_abs_path=jpg_dir_abs_path,
        camera_file_prefixs=camera_prefixes,
        jpg_exts=jpg_exts,
        if_logging=True,
    )
    logging.info(f"RST: Found Total JPG/JPEG files: {detailed_info[TOTAL_JPG_CNT]}")
    logging.info(f"RST: Found Total Camera JPG/JPEG files: {detailed_info[TOTAL_CAMERA_JPG_CNT]}")
    logging.info(f"RST: Found Unique Camera JPG/JPEG files: {detailed_info[UNIQUE_CAMERA_JPG_CNT]}")

    total_jpg_cnt: int = detailed_info[TOTAL_JPG_CNT]
    total_camera_jpg_cnt: int = detailed_info[TOTAL_CAMERA_JPG_CNT]
    unique_camera_jpg_cnt: int = detailed_info[UNIQUE_CAMERA_JPG_CNT]

    # 2. Filter raw files based on the gathered JPG names
    logging.info("Filtering RAW files...")
    detailed_info: Dict[str, int] = filter_raw_files_by_jpg_names(
        raw_dir_abs_path=raw_dir_abs_path,
        raw_exts=raw_exts,
        jpg_names=camera_jpg_names,
    )
    logging.info(f"RST: Kept RAW files: {detailed_info[KEPT_RAW_CNT]}")
    logging.info(f"RST: Deleted RAW files: {detailed_info[DELETED_RAW_CNT]}")
    logging.info(f"RST: Failed to delete RAW files: {detailed_info[FAILED_DELETE_RAW_CNT]}")

    kept_raw_cnt: int = detailed_info[KEPT_RAW_CNT]
    deleted_raw_cnt: int = detailed_info[DELETED_RAW_CNT]
    failed_delete_raw_cnt: int = detailed_info[FAILED_DELETE_RAW_CNT]

    # 3. Print the summary of the operation
    logging.info("==========================================================")
    logging.info("Script completed successfully.")
    logging.info("----------------------------------------------------------")
    logging.info(f"RST: JPG/JPEG Final counts: Total {total_jpg_cnt}, Camera {total_camera_jpg_cnt}, Unique Camera {unique_camera_jpg_cnt}.")
    logging.info(f"RST: RAW Final counts: Kept {kept_raw_cnt}, Deleted {deleted_raw_cnt}, Failed to delete {failed_delete_raw_cnt}.")
    logging.info("----------------------------------------------------------")
    logging.info("Exiting the script.")
    logging.info("==========================================================")

    # Clear logging handlers to prevent duplicate logs in future runs
    clear_logging_handlers()


if __name__ == "__main__":
    # Run the main function with the default config file path
    filter_raw_by_jpg_main(config_file_path="config/config.yaml")











