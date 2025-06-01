import os
import logging
from typing import Set, Tuple, Dict, List, Any
from pprint import pprint

from src.utils.scripts import assert_abs_paths_exist
from src.utils.scripts import gather_camera_jpg_names
from src.utils.scripts import filter_raw_files_by_jpg_names

from src.config.loader import load_config


CONFIG_FILE_PATH = "config/config.yaml"

def filter_raw_by_jpg_main():
    """
    Main function to filter raw files based on JPG names.
    """
    # Load configuration from YAML file
    config: Dict[str, Any] = load_config(CONFIG_FILE_PATH)
    # Extract configuration parameters
    jpg_dir_abs_path: str = config['jpg_dir_abs_path']
    raw_dir_abs_path: str = config['raw_dir_abs_path']
    jpg_exts: List[str] = config['jpg_exts']
    raw_exts: List[str] = config['raw_exts']
    camera_prefixes: List[str] = config['camera_prefixes']







