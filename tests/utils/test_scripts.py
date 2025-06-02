import random
import uuid
from typing import Set, List, Tuple, Dict
from pathlib import Path

from tests.base.test_base import TestScripts
from src.utils.scripts import TOTAL_JPG_CNT, TOTAL_CAMERA_JPG_CNT, UNIQUE_CAMERA_JPG_CNT
from src.utils.scripts import KEPT_RAW_CNT, DELETED_RAW_CNT, FAILED_DELETE_RAW_CNT
from src.utils.scripts import assert_abs_paths_exist
from src.utils.scripts import gather_camera_jpg_names
from src.utils.scripts import filter_raw_files_by_jpg_names


class TestAssertAbsPathsExist(TestScripts):
    def test_assert_abs_paths_exist(self):
        # Initialize existing and non-existing paths containers
        TEST_EXIST_ABS_PATH_CNT = 100
        TEST_NOT_EXIST_ABS_PATH_CNT = 100
        TEST_RANDOM_DEPTH = (1, 5)  # Random depth for directory creation
        existing_paths: List[str] = []
        not_existing_paths: List[str] = []

        # Create EXIST_ABS_PATH_CNT existing paths with different depths
        temp_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_EXIST_ABS_PATH_CNT,
            file_ext=".txt",
            file_prefix="file_",
        )
        existing_paths = list(str(path.resolve()) for path in temp_paths)

        # Create NOT_EXIST_ABS_PATH_CNT non-existing paths
        while len(not_existing_paths) < TEST_NOT_EXIST_ABS_PATH_CNT:
            fake_path = self.data_root / f"fake_{uuid.uuid4().hex[:10]}" / f"nofile_{uuid.uuid4().hex[:6]}.txt"
            if not fake_path.exists():
                not_existing_paths.append(str(fake_path.resolve()))

        # TestCase 01: All existing paths should pass
        try:
            assert_abs_paths_exist(existing_paths)
        except AssertionError as e:
            self.fail(f"assert_abs_paths_exist failed for existing paths: {e}")

        # TestCase 02: Non-existing paths should raise AssertionError
        with self.assertRaises(AssertionError) as e:
            assert_abs_paths_exist(not_existing_paths)
        self.assertIn("Path does not exist", str(e.exception))

        # TestCase 03: Mixed existing and non-existing paths should raise AssertionError
        mixed_paths = existing_paths + not_existing_paths
        with self.assertRaises(AssertionError) as e:
            assert_abs_paths_exist(mixed_paths)
        self.assertIn("Path does not exist", str(e.exception))


class TestGatherCameraJpgNames(TestScripts):
    def test_gather_jpg_names(self):
        # Initialize test parameters
        TEST_JPG_CNT = 100
        TEST_REPEATED_JPG_CNT = 10
        TEST_CAMERA_JPG_CNT = 50
        TEST_NOT_JPG_CNT = 100
        TEST_RANDOM_DEPTH = (1, 5)
        TEST_JPG_EXTS = ['.jpg', '.jpeg']
        TEST_CAMERA_FILE_PREFIXS = ['camera_', 'cam_']
        TEST_RANDOM_DEPTH = (1, 5)  # Random depth for directory creation
        jpg_names: Set[str] = []

        # Create CAMERA_JPG_CNT camera JPG files with different depths
        temp_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_CAMERA_JPG_CNT,
            file_ext=random.choice(TEST_JPG_EXTS),
            file_prefix=random.choice(TEST_CAMERA_FILE_PREFIXS)
        )
        camera_jpg_names: List[str] = list(str(path.resolve().stem) for path in temp_paths)
        # Create JPG_CNT JPG files with different depths
        temp_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_JPG_CNT - TEST_CAMERA_JPG_CNT - TEST_REPEATED_JPG_CNT,
            file_ext=random.choice(TEST_JPG_EXTS),
            file_prefix="",
        )
        jpg_names: List[str] = list(str(path.resolve().stem) for path in temp_paths)
        # Create REPEATED_JPG_CNT repeated JPG files
        repeated_camera_jpg_names: List[str] = [
            f"{camera_jpg_name}{random.choice(TEST_JPG_EXTS)}" for camera_jpg_name in camera_jpg_names[:TEST_REPEATED_JPG_CNT]
        ]
        temp_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_REPEATED_JPG_CNT,
            if_repeated=True,
            file_names=repeated_camera_jpg_names,
        )
        repeated_jpg_names: List[str] = list(str(path.resolve().stem) for path in temp_paths)
        # Create NOT_JPG_CNT non-JPG files
        temp_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_NOT_JPG_CNT,
            file_ext=".txt",
        )

        # jpg_names = set(jpg_names + camera_jpg_names + repeated_jpg_names)

        # TestCase 01: Gather JPG names from the directory
        jpg_dir_abs_path = str(self.data_root.resolve())
        gathered_camera_jpg_names, detailed_info = gather_camera_jpg_names(
            jpg_dir_abs_path=jpg_dir_abs_path,
            camera_file_prefixs=TEST_CAMERA_FILE_PREFIXS,
            jpg_exts=TEST_JPG_EXTS,
            if_logging=False
        )

        self.assertEqual(gathered_camera_jpg_names, set(camera_jpg_names))
        self.assertEqual(detailed_info[TOTAL_JPG_CNT], TEST_JPG_CNT)
        self.assertEqual(detailed_info[TOTAL_CAMERA_JPG_CNT], TEST_CAMERA_JPG_CNT + TEST_REPEATED_JPG_CNT)
        self.assertEqual(detailed_info[UNIQUE_CAMERA_JPG_CNT], TEST_CAMERA_JPG_CNT)


class TestFilterRawFilesByJpgNames(TestScripts):
    def test_filter_raw_files_by_jpg_names(self):
        # Initialize test parameters
        TEST_JPG_CNT = 100
        TEST_RAW_CNT = 300
        TEST_RANDOM_DEPTH = (1, 5)
        TEST_JPG_EXTS = ['.jpg', '.jpeg']
        TEST_RAW_EXTS = ['.nef', '.cr2', '.dng']

        TEST_JPG_DIR: Path = self.data_root / "jpg_files"
        TEST_RAW_DIR: Path = self.data_root / "raw_files"

        # Create JPG files
        jpg_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_JPG_CNT,
            file_ext=random.choice(TEST_JPG_EXTS),
            base_path=TEST_JPG_DIR,
        )
        jpg_names: List[str] = list(str(path.resolve().stem) for path in jpg_paths)

        # Create Corresponding camera JPG files
        corresponding_camera_raw_names: List[str] = [
            f"{name}{random.choice(TEST_RAW_EXTS)}" for name in jpg_names[:]
        ]
        coresponding_raw_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_JPG_CNT,
            if_repeated=True,
            file_names=corresponding_camera_raw_names,
            base_path=TEST_RAW_DIR,
        )

        # Create non-corresponding RAW files
        raw_paths: List[Path] = self.create_dummy_files(
            random_depth=TEST_RANDOM_DEPTH,
            file_count=TEST_RAW_CNT - TEST_JPG_CNT,
            file_ext=random.choice(TEST_RAW_EXTS),
            base_path=TEST_RAW_DIR,
        )

        # TestCase 01: Filter RAW files by JPG names
        detailed_info: Dict[str, int] = filter_raw_files_by_jpg_names(str(TEST_RAW_DIR.resolve()), raw_exts=TEST_RAW_EXTS, jpg_names=set(jpg_names))
        self.assertEqual(detailed_info[KEPT_RAW_CNT], TEST_JPG_CNT)
        self.assertEqual(detailed_info[DELETED_RAW_CNT], TEST_RAW_CNT - TEST_JPG_CNT)
        self.assertEqual(detailed_info[FAILED_DELETE_RAW_CNT], 0)

        remaining_raw_files: List[Path] = list(TEST_RAW_DIR.rglob(f"*"))
        remaining_raw_stems: List[str] = [path.stem for path in remaining_raw_files if path.suffix.lower() in TEST_RAW_EXTS]
        self.assertEqual(set(remaining_raw_stems), set(jpg_names))






