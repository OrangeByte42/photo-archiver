import unittest
import shutil
import random
import uuid

from pathlib import Path
from typing import List, Tuple


class TestScripts(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory for testing
        self.data_root = Path("tests/data")
        self.data_root.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory after tests
        if self.data_root.exists():
            shutil.rmtree(self.data_root)

    def create_dummy_files(self, random_depth: Tuple[int], file_count: int, file_ext: str="", file_prefix: str = "", if_repeated: bool=False, file_names: List[str]=None, base_path: Path=None) -> List[Path]:
        # If file_names is provided, use it to create files
        if if_repeated == True:
            assert file_count == len(file_names)
        # Initialize a list to hold the created file paths
        created_files: List[Path] = []
        # Create dummy files with random directory structure and specified file extension
        for i in range(file_count):
            # Generate a random depth for the directory structure
            depth: int = random.randint(*random_depth)
            sub_dirs: List[str] = [f"dir_{i}_{uuid.uuid4().hex[:4]}" for _ in range(depth)]
            path = self.data_root.joinpath(*sub_dirs) if base_path == None else base_path.joinpath(*sub_dirs)
            path.mkdir(parents=True, exist_ok=True)
            # Create a dummy file in the path
            file_name: str = ""
            if if_repeated and file_names is not None:
                file_name = file_names[i]
            else:
                file_name = f"{file_prefix}{uuid.uuid4().hex[:6]}{file_ext}"
            file_path = path / file_name
            file_path.touch()
            created_files.append(file_path.resolve())
        return created_files



