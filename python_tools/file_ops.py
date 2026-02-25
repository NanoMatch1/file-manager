from __future__ import annotations

from pathlib import Path
from typing import Iterable


def _iter_files(root: Path, extension: str | None, recursive: bool) -> Iterable[Path]:
    matcher = "**/*" if recursive else "*"
    for path in root.glob(matcher):
        if not path.is_file():
            continue
        if extension and path.suffix.lower() != extension.lower():
            continue
        yield path


def rename_files_replace(
    directory: str,
    old_key: str,
    new_key: str,
    extension: str = ".txt",
    recursive: bool = False,
    dry_run: bool = False,
) -> int:
    root = Path(directory)
    renamed = 0

    for file_path in _iter_files(root, extension, recursive):
        if old_key not in file_path.name:
            continue

        target = file_path.with_name(file_path.name.replace(old_key, new_key))
        if target == file_path:
            continue

        if not dry_run:
            file_path.rename(target)
        renamed += 1

    return renamed


def rename_files_basename(
    directory: str,
    new_basename: str,
    separator: str = "_",
    extension: str = ".txt",
    recursive: bool = False,
    dry_run: bool = False,
) -> int:
    root = Path(directory)
    renamed = 0

    for file_path in _iter_files(root, extension, recursive):
        stem_parts = file_path.stem.split(separator)
        if not stem_parts:
            continue

        new_stem = separator.join([new_basename, *stem_parts[1:]])
        new_name = f"{new_stem}{file_path.suffix}"
        target = file_path.with_name(new_name)

        if target == file_path:
            continue

        if not dry_run:
            file_path.rename(target)
        renamed += 1

    return renamed


def pad_filename_indices(
    directory: str,
    index_position: int = 1,
    pad_length: int = 3,
    pad_char: str = "0",
    separator: str = "_",
    extension: str = ".txt",
    recursive: bool = False,
    dry_run: bool = False,
) -> int:
    root = Path(directory)
    renamed = 0

    for file_path in _iter_files(root, extension, recursive):
        stem_parts = file_path.stem.split(separator)
        if index_position >= len(stem_parts):
            continue

        current = stem_parts[index_position]
        padded = current.rjust(pad_length, pad_char)
        if current == padded:
            continue

        stem_parts[index_position] = padded
        new_stem = separator.join(stem_parts)
        target = file_path.with_name(f"{new_stem}{file_path.suffix}")

        if not dry_run:
            file_path.rename(target)
        renamed += 1

    return renamed


def move_files_by_suffix(
    directory: str,
    suffixes: tuple[str, ...] = ("A", "B", "C"),
    marker: str = "_",
    extension: str = ".txt",
    dry_run: bool = False,
) -> int:
    root = Path(directory)
    moved = 0

    for file_path in root.iterdir():
        if not file_path.is_file():
            continue
        if extension and file_path.suffix.lower() != extension.lower():
            continue

        for suffix in suffixes:
            token = f"{marker}{suffix}"
            if token not in file_path.stem:
                continue

            target_dir = root / suffix
            target = target_dir / file_path.name
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                file_path.rename(target)
            moved += 1
            break

    return moved


def strip_first_column(
    directory: str,
    output_subdir: str = "edited",
    extension: str = ".txt",
    recursive: bool = True,
    header: list[str] | None = None,
) -> int:
    root = Path(directory)
    output_root = root / output_subdir
    written = 0

    for file_path in _iter_files(root, extension, recursive):
        if output_subdir in file_path.parts:
            continue

        rel = file_path.relative_to(root)
        target = output_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)

        rows: list[list[str]] = []
        with file_path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                clean = raw_line.strip()
                if not clean:
                    continue
                rows.append(clean.split(",")[1:])

        if header:
            rows.insert(0, header)

        with target.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(",".join(row) + "\n")

        written += 1

    return written
