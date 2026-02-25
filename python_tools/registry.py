from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


AddArguments = Callable[[object], None]
RunCommand = Callable[[object], int]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    category: str
    add_arguments: AddArguments
    run: RunCommand


_REGISTRY: dict[str, ToolSpec] = {}


def register_tool(spec: ToolSpec) -> None:
    if spec.name in _REGISTRY:
        raise ValueError(f"Tool '{spec.name}' is already registered.")
    _REGISTRY[spec.name] = spec


def list_tools() -> list[ToolSpec]:
    return sorted(_REGISTRY.values(), key=lambda spec: (spec.category, spec.name))


def get_tool(name: str) -> ToolSpec | None:
    return _REGISTRY.get(name)
