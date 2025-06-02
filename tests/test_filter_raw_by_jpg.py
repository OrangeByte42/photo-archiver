import random
from pathlib import Path
from typing import List

from tests.base.test_base import TestScripts
from src.filter_raw_by_jpg import filter_raw_by_jpg_main


class TestFilterRawByJpgMain(TestScripts):

    def test_filter_raw_by_jpg_main(self):
        # Initialize test parameters
        TEST_JPG_CNT = 100
        TEST_OTHER_RAW_CNT = 300
        TEST_RANDOM_DEPTH = (1, 5)
        TEST_JPG_EXTS = ['.jpg', '.jpeg']
        TEST_RAW_EXTS = ['.nef', '.cr2', '.dng']
        TEST_CAMERA_FILE_PREFIXS = ['CAM1_', 'CAM2_']
        TEST_JPG_DIR: Path = self.data_root / "jpg_files"
        TEST_RAW_DIR: Path = self.data_root / "raw_files"
        TEST_LOG_FILE: Path = self.data_root / "filter_raw_by_jpg.log"
        # Create .yaml config file
        config_file_abs_path: Path = self.data_root / "config.yaml"
        config_content = {
            'jpg_dir_abs_path': str(TEST_JPG_DIR.resolve()),
            'raw_dir_abs_path': str(TEST_RAW_DIR.resolve()),
            'jpg_exts': TEST_JPG_EXTS,
            'raw_exts': TEST_RAW_EXTS,
            'camera_prefixes': TEST_CAMERA_FILE_PREFIXS,
            'log_file_abs_path': str(TEST_LOG_FILE.resolve()),
        }
        with open(config_file_abs_path, 'w') as config_file:
            for key, value in config_content.items():
                if isinstance(value, list):
                    value = ', '.join(value)
                config_file.write(f"{key}: {value}\n")
        # Create JPG files
        jpg_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_JPG_CNT,
            file_ext=random.choice(TEST_JPG_EXTS),
            file_prefix=random.choice(TEST_CAMERA_FILE_PREFIXS),
            base_path=TEST_JPG_DIR,
        )
        jpg_names: List[str] = list(str(path.resolve().stem) for path in jpg_paths)
        corresponding_raw_names: List[str] = [
            f"{name}{random.choice(TEST_RAW_EXTS)}" for name in jpg_names[:]
        ]
        # Create Corresponding RAW files
        corresponding_raw_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_JPG_CNT,
            if_repeated=True,
            file_names=corresponding_raw_names,
            base_path=TEST_RAW_DIR,
        )
        # Create non-corresponding RAW files
        non_corresponding_raw_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_OTHER_RAW_CNT - TEST_JPG_CNT,
            file_ext=random.choice(TEST_RAW_EXTS),
            file_prefix=random.choice(TEST_CAMERA_FILE_PREFIXS),
            base_path=TEST_RAW_DIR,
        )
        # Testcase01: Run the main function
        filter_raw_by_jpg_main(config_file_path=str(config_file_abs_path.resolve()))
        remaining_raw_files: List[Path] = list(TEST_RAW_DIR.rglob(f"*"))
        remaining_raw_stems: List[str] = [path.stem for path in remaining_raw_files if path.suffix.lower() in TEST_RAW_EXTS]
        self.assertEqual(set(remaining_raw_stems), set(jpg_names))









