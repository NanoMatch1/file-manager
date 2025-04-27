# file_manager/preprocessing/move_files.py

import os

def move_files_by_suffix(filepath, suffixes=('A', 'B', 'C')):
    """Move files into subfolders A, B, and C based on filename suffix."""
    for suffix in suffixes:
        target_dir = os.path.join(filepath, suffix)
        os.makedirs(target_dir, exist_ok=True)
        matching_files = [f for f in os.listdir(filepath) if f'_{suffix}' in f]
        for file in matching_files:
            os.rename(os.path.join(filepath, file), os.path.join(target_dir, file))
