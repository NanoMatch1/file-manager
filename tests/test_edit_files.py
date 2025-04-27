import os
import pytest
from file_manager.common_tools import load_edit_and_save_files

@pytest.fixture
def edit_dir(tmp_path):
    base = tmp_path / "edit_test"
    base.mkdir()
    folder = base / "subfolder"
    folder.mkdir()
    (folder / "sample.txt").write_text("index,value1,value2\n1,10,20\n2,30,40\n")
    return base

def test_load_edit_and_save_files(edit_dir):
    load_edit_and_save_files(edit_dir, header=["header1", "header2"])
    
    edited_folder = edit_dir / "edited" / "subfolder"
    edited_file = edited_folder / "sample.txt"
    assert edited_file.exists()

    contents = edited_file.read_text().strip().splitlines()
    assert contents[0] == "header1,header2"
    assert contents[1] == "10,20"
    assert contents[2] == "30,40"
