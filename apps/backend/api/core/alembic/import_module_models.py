"""Import domain ORM modules so shared metadata is complete for Alembic."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def discover_model_module_names(modules_root: Path) -> tuple[str, ...]:
    """Return dotted names for `modules.<domain>.models.*` (skip `_*.py`).

    Returns:
        tuple[str, ...]: Dotted names for the model modules.
    """
    if not modules_root.is_dir():
        return ()

    names: list[str] = []
    for module_dir in sorted(modules_root.iterdir()):
        if not module_dir.is_dir() or module_dir.name.startswith((".", "_")):
            continue
        models_dir = module_dir / "models"
        if not models_dir.is_dir():
            continue
        for path in sorted(models_dir.rglob("*.py")):
            if path.name.startswith("_"):
                continue
            names.append(_dotted_module_name(root=modules_root, path=path))
    return tuple(names)


def import_module_models(modules_root: Path | None = None) -> tuple[str, ...]:
    """Import every discovered domain model module under ``modules_root``.

    Side effect:
    - declarative models register tables on ``OrmBaseModel.metadata``.

    Loads from file paths so discovery works for any modules root (incl. tests)
    not only the installed ``modules`` package on ``sys.path``.

    Returns imported dotted names.
    """
    root = modules_root or _default_modules_root()
    if not root.is_dir():
        return ()

    imported: list[str] = []
    for module_dir in sorted(root.iterdir()):
        if not module_dir.is_dir() or module_dir.name.startswith((".", "_")):
            continue
        models_dir = module_dir / "models"
        if not models_dir.is_dir():
            continue
        for path in sorted(models_dir.rglob("*.py")):
            if path.name.startswith("_"):
                continue
            dotted = _dotted_module_name(root=root, path=path)
            _load_module_from_path(dotted_name=dotted, path=path)
            imported.append(dotted)
    return tuple(imported)


def _default_modules_root() -> Path:
    # core/alembic/<this file> → api root → modules/
    return Path(__file__).resolve().parents[2] / "modules"


def _dotted_module_name(*, root: Path, path: Path) -> str:
    relative = path.relative_to(root).with_suffix("")
    return "modules." + ".".join(relative.parts)


def _load_module_from_path(*, dotted_name: str, path: Path) -> None:
    if dotted_name in sys.modules:
        return
    spec = importlib.util.spec_from_file_location(dotted_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(
            f"Cannot load model module {dotted_name!r} from {path}",
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[dotted_name] = module
    spec.loader.exec_module(module)
