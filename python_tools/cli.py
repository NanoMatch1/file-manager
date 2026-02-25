from __future__ import annotations

import argparse
import sys

from . import commands
from .registry import list_tools
from .scripts import load_scripts


def _build_parser() -> argparse.ArgumentParser:
    load_scripts()

    parser = argparse.ArgumentParser(
        prog="python-tools-cli",
        description="Registry-driven file processing CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-tools", help="List available core tools and scripts.")
    list_parser.set_defaults(_runner=_list_tools)

    for spec in list_tools():
        cmd_parser = subparsers.add_parser(spec.name, help=spec.description, description=spec.description)
        spec.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_runner=spec.run)

    return parser


def _list_tools(_: argparse.Namespace) -> int:
    grouped: dict[str, list[tuple[str, str]]] = {}
    for spec in list_tools():
        grouped.setdefault(spec.category, []).append((spec.name, spec.description))

    for category in sorted(grouped):
        print(f"{category}:")
        for name, description in grouped[category]:
            print(f"  {name:<24} {description}")
        print()
    return 0


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    runner = getattr(args, "_runner", None)
    if runner is None:
        parser.print_help()
        return 1
    return runner(args)


if __name__ == "__main__":
    sys.exit(main())
