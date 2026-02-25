# Custom script commands

Add new files in this folder to register custom task commands in the CLI.

## Pattern

1. Create a new module (example: `my_batch_job.py`).
2. Import `ToolSpec` and `register_tool` from `python_tools.registry`.
3. Add a function with `add_arguments` attached.

## Minimal example

```python
import argparse
from python_tools.registry import ToolSpec, register_tool


def my_job(args: argparse.Namespace) -> int:
    print(f"Running job in {args.path}")
    return 0


def _args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path")


my_job.add_arguments = _args

register_tool(
    ToolSpec(
        name="script:my-job",
        description="Run my custom batch task.",
        category="scripts",
        add_arguments=my_job.add_arguments,
        run=my_job,
    )
)
```

The CLI auto-loads all modules in `python_tools/scripts`, so new scripts appear automatically in help and `list-tools`.
