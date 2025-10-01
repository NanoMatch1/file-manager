import argparse
import sys

from file_manager import common_tools
from file_manager import maria_tools
from file_manager import temp_profile_tools

def main():
    parser = argparse.ArgumentParser(description='File Manager CLI Tools')
    subparsers = parser.add_subparsers(dest='command')

    # --- Common tools ---
    move_parser = subparsers.add_parser('move-files', help='Move files into folders A/B/C')
    move_parser.add_argument('filepath', type=str)

    rename_parser = subparsers.add_parser('rename-files', help='Rename files')
    rename_parser.add_argument('filepath', type=str)
    rename_parser.add_argument('oldKey', type=str)
    rename_parser.add_argument('newKey', type=str)

    # --- Maria-specific pipeline ---
    maria_parser = subparsers.add_parser('maria-preprocess', help='Preprocess Maria files')
    maria_parser.add_argument('filepath', type=str)

    # --- Temp-profile-specific pipeline ---
    temp_parser = subparsers.add_parser('temp-preprocess', help='Preprocess Temp Profile files')
    temp_parser.add_argument('filepath', type=str)

    args = parser.parse_args()

    if args.command == 'move-files':
        common_tools.move_files_by_suffix(args.filepath)
    elif args.command == 'rename-files':
        common_tools.rename_files(args.filepath, args.oldKey, args.newKey)
    elif args.command == 'maria-preprocess':
        maria_tools.preprocess_maria_files(args.filepath)
    elif args.command == 'temp-preprocess':
        temp_profile_tools.preprocess_temp_profile_files(args.filepath)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
