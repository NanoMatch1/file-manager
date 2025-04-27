# file_manager/preprocessing/pad_files.py

import os

def pad_file_indices(fileDir, padLength=3, padChar='0'):
    """Pad numerical indices inside filenames to fixed length."""
    folders = [f for f in os.listdir(fileDir) if os.path.isdir(os.path.join(fileDir, f))]
    for folder in folders:
        workingDir = os.path.join(fileDir, folder)
        pad_files_in_directory(workingDir, padLength, padChar)
    pad_files_in_directory(fileDir, padLength, padChar, root_only=True)

def pad_files_in_directory(directory, padLength, padChar, root_only=False):
    files = [f for f in os.listdir(directory) if f.lower().endswith('.txt')]
    if files:
        for file in files:
            parts = file.split('_')
            if len(parts) > 1:
                index = parts[1]
                new_index = index.rjust(padLength, padChar)
                new_file = file.replace(index, new_index)
                os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
        print(f'{len(files)} files renamed in {directory}.')
