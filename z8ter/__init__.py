from __future__ import annotations

__version__ = "0.2.0"

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import contextvars
import os
from starlette.templating import Jinja2Templates


# -------- App directory registry (explicit > env > cwd) --------

_APP_DIR: contextvars.ContextVar[Optional[Path]] = contextvars.ContextVar(
    "Z8TER_APP_DIR_EXPLICIT", default=None
)


def set_app_dir(path: str | Path) -> None:
    """
    Set the application root directory.
    """
    p = Path(path).resolve()
    _APP_DIR.set(p)
    _clear_cache()


def get_app_dir() -> Path:
    """
    Resolve the current application root directory.
    Precedence: explicit set_app_dir(...) > env Z8TER_APP_DIR > cwd()
    """
    explicit = _APP_DIR.get()
    if explicit is not None:
        return explicit
    env = os.getenv("Z8TER_APP_DIR")
    return Path(env).resolve() if env else Path.cwd().resolve()


# -------- Path resolution (single source of truth) --------

@dataclass(frozen=True)
class Paths:
    base: Path
    views: Path
    templates: Path
    static: Path
    api: Path
    ts: Path


def _resolve_paths(base: Path) -> Paths:
    base = base.resolve()
    return Paths(
        base=base,
        views=base / "endpoints" / "views",
        templates=base / "templates",
        static=base / "static",
        api=base / "endpoints" / "api",
        ts=base / "src" / "ts",
    )


_paths_cache: Optional[Paths] = None


def _current_paths() -> Paths:
    global _paths_cache
    base = get_app_dir()
    if _paths_cache is None or _paths_cache.base != base:
        _paths_cache = _resolve_paths(base)
    return _paths_cache


def _clear_cache() -> None:
    global _paths_cache, _templates_cache
    _paths_cache = None
    _templates_cache = None


# -------- Lazy module attributes (PEP 562) --------

_templates_cache: Optional[Jinja2Templates] = None


def get_templates() -> Jinja2Templates:
    """
    Build or return cached Jinja2Templates bound to the current templates dir.
    Recomputed if set_app_dir(...) changes.
    """
    global _templates_cache
    if _templates_cache is None:
        tdir = _current_paths().templates
        _templates_cache = Jinja2Templates(directory=str(tdir))
    return _templates_cache


def __getattr__(name: str) -> Any:
    paths = _current_paths()
    mapping: Dict[str, Path] = {
        "BASE_DIR": paths.base,
        "VIEWS_DIR": paths.views,
        "TEMPLATES_DIR": paths.templates,
        "STATIC_PATH": paths.static,
        "API_DIR": paths.api,
        "TS_DIR": paths.ts,
    }
    if name in mapping:
        return mapping[name]
    if name == "templates":
        return get_templates()
    raise AttributeError(f"module 'z8ter' has no attribute {name!r}")


__all__ = [
    "__version__",
    "set_app_dir",
    "get_app_dir",
    "get_templates"
]
