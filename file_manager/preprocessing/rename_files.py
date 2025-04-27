# file_manager/preprocessing/rename_files.py

import os

def rename_files(fileDir, oldKey, newKey, extension='.txt'):
    """Rename files replacing oldKey with newKey."""
    files = [f for f in os.listdir(fileDir) if f.lower().endswith(extension)]
    if files:
        for file in files:
            new_name = file.replace(oldKey, newKey)
            os.rename(os.path.join(fileDir, file), os.path.join(fileDir, new_name))
        print(f'{len(files)} files renamed in {fileDir}.')
    else:
        print(f'No matching files found in {fileDir}.')

def rename_files_basename(fileDir, newKey):
    """Rename files to start with a new basename key."""
    folders = [f for f in os.listdir(fileDir) if os.path.isdir(os.path.join(fileDir, f))]
    for folder in folders:
        workingDir = os.path.join(fileDir, folder)
        files = os.listdir(workingDir)
        for file in files:
            parts = file.split('_')[1:]
            new_name = '_'.join([newKey, *parts])
            os.rename(os.path.join(workingDir, file), os.path.join(workingDir, new_name))
        print(f'{len(files)} files renamed in {workingDir}.')
