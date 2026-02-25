from __future__ import annotations

import importlib
import pkgutil


_LOADED = False


def load_scripts() -> None:
    global _LOADED
    if _LOADED:
        return

    for module in pkgutil.iter_modules(__path__):
        if module.name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{module.name}")

    _LOADED = True
