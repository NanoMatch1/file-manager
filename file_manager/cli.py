# file_manager/cli.py
import argparse
import sys
from file_manager import (
    preprocess_maria_files,
    move_files_by_suffix,
    rename_files,
    rename_files_basename,
    pad_file_indices,
    load_edit_and_save_files,
)

def main():
    parser = argparse.ArgumentParser(description='File Manager CLI Tools')
    subparsers = parser.add_subparsers(dest='command')

    # Preprocess
    preprocess_parser = subparsers.add_parser('preprocess', help='Run full preprocessing pipeline')
    preprocess_parser.add_argument('filepath', type=str, help='Path to the data directory')

    # Move files
    move_parser = subparsers.add_parser('move-files', help='Move files into A, B, C folders')
    move_parser.add_argument('filepath', type=str, help='Path to the data directory')

    # Rename files
    rename_parser = subparsers.add_parser('rename-files', help='Rename files')
    rename_parser.add_argument('filepath', type=str, help='Path to the data directory')
    rename_parser.add_argument('oldKey', type=str, help='Old key to replace')
    rename_parser.add_argument('newKey', type=str, help='New key to insert')

    args = parser.parse_args()

    if args.command == 'preprocess':
        preprocess_maria_files(args.filepath)
    elif args.command == 'move-files':
        move_files_by_suffix(args.filepath)
    elif args.command == 'rename-files':
        rename_files(args.filepath, args.oldKey, args.newKey)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
