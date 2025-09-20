"""Z8ter framework package root.

Provides:
- Version info (`__version__`).
- App directory management (`set_app_dir`, `get_app_dir`).
- Centralized project path resolution (views, templates, static, api, ts).
- Cached Jinja2 template environment (`get_templates`).
- Lazy attributes (PEP 562) for common paths and templates.

Conventions:
- App root precedence: explicit `set_app_dir(...)` > env `Z8TER_APP_DIR` > cwd().
- Paths assume the standard Z8ter layout:
    <base>/
      endpoints/views/
      endpoints/api/
      templates/
      static/
      src/ts/
"""

from __future__ import annotations

__version__ = "0.2.4"

import contextvars
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlette.templating import Jinja2Templates

# -------- App directory registry (explicit > env > cwd) --------

# Context-local explicit app directory. If unset, fallback is env or cwd.
_APP_DIR: contextvars.ContextVar[Path | None] = contextvars.ContextVar(
    "Z8TER_APP_DIR_EXPLICIT", default=None
)


def set_app_dir(path: str | Path) -> None:
    """Set the application root directory.

    Args:
        path: Absolute or relative path to the project root.

    Notes:
        - Updates a context-local value, so different contexts may override it.
        - Clears caches so subsequent lookups reflect the new base.

    """
    p = Path(path).resolve()
    _APP_DIR.set(p)
    _clear_cache()


def get_app_dir() -> Path:
    """Resolve the current application root directory.

    Precedence:
        1) explicit via `set_app_dir(...)`
        2) env var `Z8TER_APP_DIR`
        3) `Path.cwd()`

    Returns:
        Absolute `Path` to the app root.

    """
    explicit = _APP_DIR.get()
    if explicit is not None:
        return explicit
    env = os.getenv("Z8TER_APP_DIR")
    return Path(env).resolve() if env else Path.cwd().resolve()


# -------- Path resolution (single source of truth) --------


@dataclass(frozen=True)
class Paths:
    """Resolved project paths derived from the app base directory."""

    base: Path
    views: Path
    templates: Path
    static: Path
    api: Path
    ts: Path


def _resolve_paths(base: Path) -> Paths:
    """Compute all derived paths from a base directory."""
    base = base.resolve()
    return Paths(
        base=base,
        views=base / "endpoints" / "views",
        templates=base / "templates",
        static=base / "static",
        api=base / "endpoints" / "api",
        ts=base / "src" / "ts",
    )


_paths_cache: Paths | None = None


def _current_paths() -> Paths:
    """Return cached paths for the current app dir; recompute on base change."""
    global _paths_cache
    base = get_app_dir()
    if _paths_cache is None or _paths_cache.base != base:
        _paths_cache = _resolve_paths(base)
    return _paths_cache


def _clear_cache() -> None:
    """Clear cached paths and template environment (called on base change)."""
    global _paths_cache, _templates_cache
    _paths_cache = None
    _templates_cache = None


# -------- Lazy module attributes (PEP 562) --------

_templates_cache: Jinja2Templates | None = None


def get_templates() -> Jinja2Templates:
    """Return a cached `Jinja2Templates` bound to the current templates dir.

    The cache is invalidated automatically when `set_app_dir(...)` updates the
    base directory.

    Returns:
        A `Jinja2Templates` instance rooted at the resolved templates folder.

    """
    global _templates_cache
    if _templates_cache is None:
        tdir = _current_paths().templates
        _templates_cache = Jinja2Templates(directory=str(tdir))
    return _templates_cache


def __getattr__(name: str) -> Any:
    """Expose common path aliases and `templates` lazily.

    Supported names:
        - "BASE_DIR", "VIEWS_DIR", "TEMPLATES_DIR", "STATIC_PATH",
          "API_DIR", "TS_DIR": return `Path` objects.
        - "templates": return `Jinja2Templates` (same as `get_templates()`).

    Raises:
        AttributeError: If the attribute is not recognized.

    """
    paths = _current_paths()
    mapping: dict[str, Path] = {
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


__all__ = ["__version__", "set_app_dir", "get_app_dir", "get_templates"]
