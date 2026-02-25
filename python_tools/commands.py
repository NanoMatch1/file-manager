from __future__ import annotations

import argparse

from .file_ops import (
    move_files_by_suffix,
    pad_filename_indices,
    rename_files_basename,
    rename_files_replace,
    strip_first_column,
)
from .registry import ToolSpec, register_tool


def rename_command(args: argparse.Namespace) -> int:
    count = rename_files_replace(
        directory=args.path,
        old_key=args.old,
        new_key=args.new,
        extension=args.ext,
        recursive=args.recursive,
        dry_run=args.dry_run,
    )
    print(f"Renamed {count} file(s).")
    return 0


def _rename_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument("old", help="Substring to replace.")
    parser.add_argument("new", help="Replacement substring.")
    parser.add_argument("--ext", default=".txt", help="File extension filter.")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories too.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing changes.")


rename_command.add_arguments = _rename_args
register_tool(
    ToolSpec(
        name="rename",
        description="Rename files by replacing a key in filenames.",
        category="core",
        add_arguments=rename_command.add_arguments,
        run=rename_command,
    )
)


def rename_basename_command(args: argparse.Namespace) -> int:
    count = rename_files_basename(
        directory=args.path,
        new_basename=args.basename,
        separator=args.sep,
        extension=args.ext,
        recursive=args.recursive,
        dry_run=args.dry_run,
    )
    print(f"Renamed {count} file(s).")
    return 0


def _rename_basename_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument("basename", help="New basename.")
    parser.add_argument("--sep", default="_", help="Filename separator.")
    parser.add_argument("--ext", default=".txt", help="File extension filter.")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories too.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing changes.")


rename_basename_command.add_arguments = _rename_basename_args
register_tool(
    ToolSpec(
        name="rename-basename",
        description="Replace filename basename before the first separator.",
        category="core",
        add_arguments=rename_basename_command.add_arguments,
        run=rename_basename_command,
    )
)


def pad_index_command(args: argparse.Namespace) -> int:
    count = pad_filename_indices(
        directory=args.path,
        index_position=args.position,
        pad_length=args.length,
        pad_char=args.char,
        separator=args.sep,
        extension=args.ext,
        recursive=args.recursive,
        dry_run=args.dry_run,
    )
    print(f"Renamed {count} file(s).")
    return 0


def _pad_index_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument("--position", type=int, default=1, help="Segment index to pad.")
    parser.add_argument("--length", type=int, default=3, help="Total width after padding.")
    parser.add_argument("--char", default="0", help="Padding character.")
    parser.add_argument("--sep", default="_", help="Filename separator.")
    parser.add_argument("--ext", default=".txt", help="File extension filter.")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories too.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing changes.")


pad_index_command.add_arguments = _pad_index_args
register_tool(
    ToolSpec(
        name="pad-index",
        description="Pad one filename segment to fixed width.",
        category="core",
        add_arguments=pad_index_command.add_arguments,
        run=pad_index_command,
    )
)


def move_by_suffix_command(args: argparse.Namespace) -> int:
    count = move_files_by_suffix(
        directory=args.path,
        suffixes=tuple(args.suffixes),
        marker=args.marker,
        extension=args.ext,
        dry_run=args.dry_run,
    )
    print(f"Moved {count} file(s).")
    return 0


def _move_by_suffix_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument(
        "--suffixes",
        nargs="+",
        default=["A", "B", "C"],
        help="Suffix tokens to route into folders.",
    )
    parser.add_argument("--marker", default="_", help="Marker before suffix in filename.")
    parser.add_argument("--ext", default=".txt", help="File extension filter.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing changes.")


move_by_suffix_command.add_arguments = _move_by_suffix_args
register_tool(
    ToolSpec(
        name="move-by-suffix",
        description="Move files into subfolders by suffix markers (A/B/C, etc).",
        category="core",
        add_arguments=move_by_suffix_command.add_arguments,
        run=move_by_suffix_command,
    )
)


def strip_first_column_command(args: argparse.Namespace) -> int:
    count = strip_first_column(
        directory=args.path,
        output_subdir=args.output,
        extension=args.ext,
        recursive=args.recursive,
    )
    print(f"Wrote {count} file(s).")
    return 0


def _strip_first_column_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument("--output", default="edited", help="Output folder name.")
    parser.add_argument("--ext", default=".txt", help="File extension filter.")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories too.")


strip_first_column_command.add_arguments = _strip_first_column_args
register_tool(
    ToolSpec(
        name="strip-first-column",
        description="Create edited output files with first CSV column removed.",
        category="core",
        add_arguments=strip_first_column_command.add_arguments,
        run=strip_first_column_command,
    )
)
