# file_manager/cli.py

import typer
from file_manager import common_tools, maria_tools, temp_profile_tools

app = typer.Typer(help="File Manager CLI: rename, move, preprocess files easily.")

@app.command()
def move_files(filepath: str):
    """
    Move files into subfolders A/B/C based on suffix in filename.
    """
    common_tools.move_files_by_suffix(filepath)

@app.command()
def rename_files(filepath: str, oldkey: str, newkey: str):
    """
    Rename files inside a directory, replacing oldkey with newkey.
    """
    common_tools.rename_files(filepath, oldkey, newkey)

@app.command()
def maria_preprocess(filepath: str):
    """
    Full preprocessing pipeline for Maria's data.
    Moves, renames, pads, and edits files with Maria-specific settings.
    """
    maria_tools.preprocess_maria_files(filepath)

@app.command()
def temp_preprocess(filepath: str):
    """
    Full preprocessing pipeline for Temperature Profile experiments.
    """
    temp_profile_tools.preprocess_temp_profile_files(filepath)

if __name__ == "__main__":
    app()
