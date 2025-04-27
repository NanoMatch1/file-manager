import os
import pytest
from file_manager.common_tools import pad_file_indices

@pytest.fixture
def pad_dir(tmp_path):
    base = tmp_path / "pad_test"
    base.mkdir()
    (base / "LnNP_1.txt").write_text("Pad test")
    (base / "LnNP_23.txt").write_text("Pad test")
    return base

def test_pad_file_indices(pad_dir):
    pad_file_indices(pad_dir, padLength=3, padChar="0")
    
    assert (pad_dir / "LnNP_001.txt").exists()
    assert (pad_dir / "LnNP_023.txt").exists()