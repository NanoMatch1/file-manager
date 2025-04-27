# file_manager/preprocessing/move_files.py

import os
import typer

def move_files_by_suffix(filepath, suffixes=('A', 'B', 'C')):
    """Move files into subfolders."""
    if not os.path.exists(filepath):
        typer.echo(f"Error: Directory {filepath} does not exist.", err=True)
        raise typer.Exit(code=1)

    for suffix in suffixes:
        target_dir = os.path.join(filepath, suffix)
        os.makedirs(target_dir, exist_ok=True)
        matching_files = [f for f in os.listdir(filepath) if f'_{suffix}' in f]
        for file in matching_files:
            src = os.path.join(filepath, file)
            dst = os.path.join(target_dir, file)
            try:
                os.rename(src, dst)
            except Exception as e:
                typer.echo(f"Failed to move {file}: {e}", err=True)

    typer.echo(f"Moved files into {', '.join(suffixes)} folders.")
