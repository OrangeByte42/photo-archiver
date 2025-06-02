import os
import logging
from typing import Set, Tuple, Dict, List

from send2trash import send2trash


TOTAL_JPG_CNT = 'total_jpg_cnt'
TOTAL_CAMERA_JPG_CNT = 'total_camera_jpg_cnt'
UNIQUE_CAMERA_JPG_CNT = 'unique_camera_jpg_cnt'

KEPT_RAW_CNT = 'kept_raw_cnt'
DELETED_RAW_CNT = 'deleted_raw_cnt'
FAILED_DELETE_RAW_CNT = 'failed_delete_raw_cnt'

def assert_abs_paths_exist(abs_paths: List[str]) -> None:
    """
    Assert that all absolute paths in the list exist.

    :param abs_paths: List of absolute paths to check.
    :raises AssertionError: If any path does not exist.
    """
    for abs_path in abs_paths:
        if not os.path.exists(abs_path):
            logging.error(f"Path does not exist: {abs_path}")
            raise AssertionError(f"Path does not exist: {abs_path}")

def gather_camera_jpg_names(jpg_dir_abs_path: str, camera_file_prefixs: List[str], jpg_exts: List[str], if_logging: bool=True) -> Tuple[Set[str], Dict[str, int]]:
    """
    Recursively gather all JPG/JPEG file names (without extensions) in the specified directory.

    :param jpg_dir_abs_path: Absolute path to the directory containing JPG files.
    :param camera_file_prefixs: List of camera file prefixes to filter the files.
    :param jpg_exts: List of file extensions to consider (e.g., ['.jpg', '.jpeg']).
    :return: A tuple containing:
        - A set of unique file names (without extensions).
        - A dictionary containing more detailed information about the JPG directory:
            - 'total_jpg_cnt': Total number of JPG/JPEG files found (with specific extensions name).
            - 'total_camera_jpg_cnt': Total number of camera JPG/JPEG files found (with specific prefixes).
            - 'unique_camera_jpg_cnt': Number of unique camera JPG/JPEG files found.
    """
    # Preprocess the input parameters
    camera_file_prefixs: Tuple[str] = tuple(prefix.lower() for prefix in camera_file_prefixs)
    jpg_exts: Tuple[str] = tuple(ext.lower() for ext in jpg_exts)

    # Initialize variables
    camera_jpg_names: Set[str] = set()
    total_jpg_cnt: int = 0
    total_camera_jpg_cnt: int = 0
    unique_camera_jpg_cnt: int = 0

    # Start to work on the directory
    for _1, _2, files in os.walk(jpg_dir_abs_path):
        for filename in files:
            # Check the file extension
            if not filename.lower().endswith(jpg_exts):
                continue
            total_jpg_cnt += 1
            # Get the file name without extension
            file_name_without_ext = os.path.splitext(filename)[0]
            # Add the file name to the set if it starts with any of the camera prefixes
            if file_name_without_ext.lower().startswith(camera_file_prefixs):
                total_camera_jpg_cnt += 1
                camera_jpg_names.add(file_name_without_ext)
                if if_logging:
                    logging.info(f"Found JPG/JPEG file: {file_name_without_ext}, name added to the set.")

    # Build the detailed information dictionary
    unique_camera_jpg_cnt = len(camera_jpg_names)
    detailed_info: Dict[str, int] = {
        TOTAL_JPG_CNT: total_jpg_cnt,
        TOTAL_CAMERA_JPG_CNT: total_camera_jpg_cnt,
        UNIQUE_CAMERA_JPG_CNT: unique_camera_jpg_cnt,
    }

    # Return the JPG/JPEG names and the detailed information dictionary
    return camera_jpg_names, detailed_info

def filter_raw_files_by_jpg_names(raw_dir_abs_path: str, raw_exts: List[str], jpg_names: Set[str]) -> Dict[str, int]:
    """
    Recursively filter out RAW files in the specified directory that do not have corresponding JPG/JPEG files.

    :param raw_dir_abs_path: Path to the directory containing RAW files.
    :param raw_exts: List of file extensions to consider for RAW files (e.g., ['.cr2', '.nef']).
    :param jpg_names: Set of JPG/JPEG file names (without extensions) to check against.
    :return: A dictionary containing:
        - 'kept_raw_cnt': Number of RAW files kept (not deleted).
        - 'deleted_raw_cnt': Number of RAW files deleted (moved to Recycle Bin).
        - 'failed_delete_raw_cnt': Number of RAW files that failed to delete.
    """
    # Preprocess the input parameters
    raw_exts: Tuple[str] = tuple(ext.lower() for ext in raw_exts)

    # Initialize variables
    kept_raw_cnt: int = 0
    deleted_raw_cnt: int = 0
    failed_delete_raw_cnt: int = 0

    # Recursively walk through the directory
    for root, _2, files in os.walk(raw_dir_abs_path):
        for filename in files:
            # Check if the file is a RAW file based on its extension
            if not filename.lower().endswith(raw_exts):
                continue
            # Get the file name without the extension
            name: str = os.path.splitext(filename)[0]
            # Check if the file name is in the set of JPG names
            if name in jpg_names:
                kept_raw_cnt += 1
                logging.info(f"Keeping RAW file: {filename}, name found in JPG/JPEG names set.")
            else:
                try:
                    # Move the RAW file to the Recycle Bin
                    send2trash(os.path.join(root, filename))
                    deleted_raw_cnt += 1
                    logging.info(f"Deleted RAW file: {filename}, name not found in JPG/JPEG names set.")
                except Exception as e:
                    # If moving the file to the Recycle Bin fails, increment the failed count
                    failed_delete_raw_cnt += 1
                    logging.error(f"Failed to delete RAW file: {os.path.join(root, filename)} to Recycle Bin. Error: {e}")

    # Build the detailed information dictionary
    detailed_info: Dict[str, int] = {
        KEPT_RAW_CNT: kept_raw_cnt,
        DELETED_RAW_CNT: deleted_raw_cnt,
        FAILED_DELETE_RAW_CNT: failed_delete_raw_cnt,
    }

    # Return the detailed information dictionary
    return detailed_info













