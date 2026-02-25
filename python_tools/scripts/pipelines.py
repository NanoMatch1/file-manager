from __future__ import annotations

import argparse

from ..file_ops import (
    move_files_by_suffix,
    pad_filename_indices,
    rename_files_basename,
    strip_first_column,
)
from ..registry import ToolSpec, register_tool


def _run_pipeline(path: str, key: str, header: list[str], dry_run: bool) -> dict[str, int]:
    moved = move_files_by_suffix(path, suffixes=("A", "B", "C"), dry_run=dry_run)
    renamed = rename_files_basename(path, new_basename=key, recursive=True, dry_run=dry_run)
    padded = pad_filename_indices(path, pad_length=3, pad_char="0", recursive=True, dry_run=dry_run)
    written = 0

    if not dry_run:
        written = strip_first_column(path, output_subdir="edited", recursive=True, header=header)

    return {"moved": moved, "renamed": renamed, "padded": padded, "written": written}


def maria_preprocess(args: argparse.Namespace) -> int:
    stats = _run_pipeline(
        path=args.path,
        key="LnNP",
        header=["data_type", "maria"],
        dry_run=args.dry_run,
    )
    print(
        f"Moved {stats['moved']} | Renamed {stats['renamed']} | "
        f"Padded {stats['padded']} | Wrote {stats['written']}"
    )
    return 0


def _maria_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument("--dry-run", action="store_true", help="Preview rename/move steps only.")


maria_preprocess.add_arguments = _maria_args
register_tool(
    ToolSpec(
        name="script:maria-preprocess",
        description="Pipeline for Maria files (move, rename, pad, edited output).",
        category="scripts",
        add_arguments=maria_preprocess.add_arguments,
        run=maria_preprocess,
    )
)


def temp_preprocess(args: argparse.Namespace) -> int:
    stats = _run_pipeline(
        path=args.path,
        key="TempProfile",
        header=["data_type", "temp_profile"],
        dry_run=args.dry_run,
    )
    print(
        f"Moved {stats['moved']} | Renamed {stats['renamed']} | "
        f"Padded {stats['padded']} | Wrote {stats['written']}"
    )
    return 0


def _temp_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", help="Target directory.")
    parser.add_argument("--dry-run", action="store_true", help="Preview rename/move steps only.")


temp_preprocess.add_arguments = _temp_args
register_tool(
    ToolSpec(
        name="script:temp-preprocess",
        description="Pipeline for temperature profile files.",
        category="scripts",
        add_arguments=temp_preprocess.add_arguments,
        run=temp_preprocess,
    )
)
