import os
import shutil
import pytest
from file_manager.common_tools import move_files_by_suffix

@pytest.fixture
def test_dir(tmp_path):
    # Setup: create a temp directory with files
    base = tmp_path / "data"
    base.mkdir()
    (base / "sample_A.txt").write_text("Test A")
    (base / "sample_B.txt").write_text("Test B")
    (base / "sample_C.txt").write_text("Test C")
    return base

def test_move_files(test_dir):
    move_files_by_suffix(test_dir)

    assert (test_dir / "A" / "sample_A.txt").exists()
    assert (test_dir / "B" / "sample_B.txt").exists()
    assert (test_dir / "C" / "sample_C.txt").exists()
