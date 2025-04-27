# file_manager/maria_tools.py

from file_manager.common_tools import (
    move_files_by_suffix,
    rename_files_basename,
    pad_file_indices,
    load_edit_and_save_files,
)

def preprocess_maria_files(filepath):
    """Full preprocessing pipeline for Maria's data."""
    move_files_by_suffix(filepath)
    rename_files_basename(filepath, newKey='LnNP')
    pad_file_indices(filepath, padLength=3, padChar='0')
    load_edit_and_save_files(filepath, header=['data_type', 'maria'])

