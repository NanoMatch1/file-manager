import os
import json

def list_folders(directory):
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def list_files(directory, extension=None):
    if extension:
        return [f for f in os.listdir(directory) if f.lower().endswith(extension.lower())]
    return [f for f in os.listdir(directory)]

# -- File renaming utilities --

def rename_files_basename(fileDir, newKey):
    folders = list_folders(fileDir)
    for folder in folders:
        workingDir = os.path.join(fileDir, folder)
        files = list_files(workingDir)
        for file in files:
            parts = file.split('_')[1:]
            new_name = '_'.join([newKey, *parts])
            os.rename(os.path.join(workingDir, file), os.path.join(workingDir, new_name))
        print(f'{len(files)} files renamed in {workingDir}.')

def pad_file_indices(fileDir, padLength=3, padChar='0'):
    folders = list_folders(fileDir)
    for folder in folders:
        workingDir = os.path.join(fileDir, folder)
        pad_files_in_directory(workingDir, padLength, padChar)
    pad_files_in_directory(fileDir, padLength, padChar, root_only=True)

def pad_files_in_directory(directory, padLength, padChar, root_only=False):
    files = list_files(directory, extension='.txt')
    if files:
        for file in files:
            parts = file.split('_')
            if len(parts) > 1:
                index = parts[1]
                new_index = index.rjust(padLength, padChar)
                new_file = file.replace(index, new_index)
                os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
        print(f'{len(files)} files renamed in {directory}.')


def rename_files(fileDir, oldKey, newKey, extension='.txt'):
    files = list_files(fileDir, extension)
    if files:
        for file in files:
            new_name = file.replace(oldKey, newKey)
            os.rename(os.path.join(fileDir, file), os.path.join(fileDir, new_name))
        print(f'{len(files)} files renamed in {fileDir}.')
    else:
        folders = list_folders(fileDir)
        for idx, folder in enumerate(folders):
            workingDir = os.path.join(fileDir, folder)
            files = list_files(workingDir)
            for file in files:
                new_name = file.replace(oldKey, newKey)
                os.rename(os.path.join(workingDir, file), os.path.join(workingDir, new_name))
            print(f'{len(files)} files renamed in {workingDir}.')

# -- File moving utilities --

def move_files_by_suffix(filepath, suffixes=('A', 'B', 'C')):
    for suffix in suffixes:
        target_dir = os.path.join(filepath, suffix)
        os.makedirs(target_dir, exist_ok=True)
        matching_files = [f for f in os.listdir(filepath) if f'_{suffix}' in f]
        for file in matching_files:
            os.rename(os.path.join(filepath, file), os.path.join(target_dir, file))

# -- Data loading and editing --

def add_header(data, header):
    if header:
        return [header] + data
    return data

def load_edit_and_save_files(filepath, header=None):
    export_dir = os.path.join(filepath, 'edited')
    os.makedirs(export_dir, exist_ok=True)
    folders = list_folders(filepath)

    for folder in folders:
        working_dir = os.path.join(filepath, folder)
        export_folder = os.path.join(export_dir, folder)
        os.makedirs(export_folder, exist_ok=True)

        files = list_files(working_dir, extension='.txt')
        for file in files:
            with open(os.path.join(working_dir, file), 'r') as f:
                lines = f.readlines()

            data = [line.strip('\n').split(',')[1:] for line in lines if line.strip()]
            data = add_header(data, header)

            with open(os.path.join(export_folder, file), 'w') as f:
                for row in data:
                    f.write(','.join(row) + '\n')

            print(f'{file} edited and saved to {export_folder}.')

# -- Configuration (placeholder) --

def config_json(filepath):
    # To be implemented
    pass

# -- Processing pipelines --

def preprocess_files(filepath):
    move_files_by_suffix(filepath)
    rename_files_basename(filepath, newKey='LnNP')
    pad_file_indices(filepath, padLength=3, padChar='0')
    load_edit_and_save_files(filepath, header=['data_type', 'maria'])
