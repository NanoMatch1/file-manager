import os
import pytest
from file_manager.common_tools import rename_files, rename_files_basename

@pytest.fixture
def rename_dir(tmp_path):
    base = tmp_path / "rename_test"
    base.mkdir()
    (base / "old_key_001.txt").write_text("Dummy content")
    return base

def test_rename_files(rename_dir):
    rename_files(rename_dir, "old_key", "new_key")
    assert (rename_dir / "new_key_001.txt").exists()

@pytest.fixture
def basename_dir(tmp_path):
    base = tmp_path / "basename_test"
    base.mkdir()
    folder = base / "subfolder"
    folder.mkdir()
    (folder / "abc_001.txt").write_text("Content")
    return base

def test_rename_files_basename(basename_dir):
    rename_files_basename(basename_dir, "LnNP")
    assert (basename_dir / "subfolder" / "LnNP_001.txt").exists()
