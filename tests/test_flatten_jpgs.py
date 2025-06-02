import random
from pathlib import Path
from typing import List, Dict, Set

from tests.base.test_base import TestScripts
from src.flatten_jpgs import flatten_jpgs_main


class TestFlattenJpgsMain(TestScripts):

    def test_flatten_jpgs_main(self):
        # Initialize test parameters
        TEST_JPG_CNT = 100
        TEST_RANDOM_DEPTH = (0, 3)
        TEST_NUMBER_OF_DIGITS = 2
        TEST_JPG_EXTS = ['.jpg', '.jpeg']
        TEST_INPUT_JPG_DIR: Path = self.data_root / "input_jpg_files"
        TEST_OUTPUT_JPG_DIR: Path = self.data_root / "output_jpg_files"
        TEST_LOG_FILE: Path = self.data_root / "flatten_jpgs.log"

        TEST_INPUT_JPG_DIR.mkdir(parents=True, exist_ok=True)
        TEST_OUTPUT_JPG_DIR.mkdir(parents=True, exist_ok=True)
        # Create .yaml config file
        config_file_abs_path: Path = self.data_root / "config.yaml"
        config_content = {
            'input_jpg_dir_abs_path': str(TEST_INPUT_JPG_DIR.resolve()),
            'output_jpg_dir_abs_path': str(TEST_OUTPUT_JPG_DIR.resolve()),
            'jpg_exts': TEST_JPG_EXTS,
            'number_of_digits': TEST_NUMBER_OF_DIGITS,
            'log_file_abs_path': str(TEST_LOG_FILE.resolve()),
        }
        with open(config_file_abs_path, 'w') as config_file:
            for key, value in config_content.items():
                if isinstance(value, list):
                    value = ', '.join(value)
                config_file.write(f"{key}: {value}\n")
        # Create JPG files
        jpg_paths: List[Path] = self.create_dummy_files(
            file_count=TEST_JPG_CNT,
            random_depth=TEST_RANDOM_DEPTH,
            file_ext=random.choice(TEST_JPG_EXTS),
            base_path=TEST_INPUT_JPG_DIR,
        )

        # Create expected names and counters
        expected_name_counter: Dict[str, int] = {}
        expected_names: Set[str] = set()
        for input_file in jpg_paths:
            relative_path = input_file.relative_to(TEST_INPUT_JPG_DIR.resolve())
            prefix = "-".join(relative_path.parts[:-1]) if relative_path.parts else ""
            expected_name_counter.setdefault(prefix, 0)
            expected_name_counter[prefix] += 1
            seq = expected_name_counter[prefix]
            ext = input_file.suffix.lower()
            new_jpg_name = f"{prefix}-{seq:0{TEST_NUMBER_OF_DIGITS}d}{ext}" if prefix else f"{seq:0{TEST_NUMBER_OF_DIGITS}d}{ext}"
            expected_names.add(new_jpg_name)

        # TestCase01: Run the main function
        flatten_jpgs_main(config_file_path=str(config_file_abs_path.resolve()))

        output_flattened_jpgs: List[Path] = list(TEST_OUTPUT_JPG_DIR.glob('*'))
        flattened_jpgs_names: List[str] = [path.name for path in output_flattened_jpgs]
        self.assertEqual(len(flattened_jpgs_names), TEST_JPG_CNT)

        actual_names: Set[str] = set(flattened_jpgs_names)
        self.assertSetEqual(actual_names, expected_names)




