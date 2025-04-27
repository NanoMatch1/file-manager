# file_manager/temp_profile_tools.py

from file_manager.common_tools import (
    move_files_by_suffix,
    rename_files_basename,
    pad_file_indices,
    load_edit_and_save_files,
)

def preprocess_temp_profile_files(filepath):
    """Full preprocessing pipeline for Temperature Profile experiments."""
    move_files_by_suffix(filepath)
    rename_files_basename(filepath, newKey='TempProfile')
    pad_file_indices(filepath, padLength=3, padChar='0')
    load_edit_and_save_files(filepath, header=['data_type', 'temp_profile'])
