# file_manager/preprocessing/edit_files.py

import os

def load_edit_and_save_files(filepath, header=None):
    """Load, edit, and save text files with optional header insertion."""
    export_dir = os.path.join(filepath, 'edited')
    os.makedirs(export_dir, exist_ok=True)
    folders = [f for f in os.listdir(filepath) if os.path.isdir(os.path.join(filepath, f))]

    for folder in folders:
        working_dir = os.path.join(filepath, folder)
        export_folder = os.path.join(export_dir, folder)
        os.makedirs(export_folder, exist_ok=True)

        files = [f for f in os.listdir(working_dir) if f.lower().endswith('.txt')]
        for file in files:
            with open(os.path.join(working_dir, file), 'r') as f:
                lines = f.readlines()

            data = [line.strip().split(',')[1:] for line in lines if line.strip()]
            if header:
                data.insert(0, header)

            with open(os.path.join(export_folder, file), 'w') as f:
                for row in data:
                    f.write(','.join(row) + '\\n')

            print(f'{file} edited and saved to {export_folder}.')
