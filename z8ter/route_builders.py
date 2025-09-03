from __future__ import annotations
import importlib
import importlib.util
import inspect
import os
from pathlib import Path
from typing import Iterable, Type, Tuple, List, Optional
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.endpoints import HTTPEndpoint
from z8ter import STATIC_PATH
from z8ter.endpoints.api import API
from z8ter.endpoints.view import View


# ---------- helpers ----------

def _resolve_roots(pkg_or_path: str) -> Tuple[Optional[str], List[str]]:
    """
    If pkg_or_path is a Python package (e.g., 'endpoints.views')
        return (pkg_name, [roots]).
    If it's a filesystem path ('endpoints/views')
        return (None, [abs_path]).
    Raise if neither can be located.
    """
    if os.path.sep in pkg_or_path or pkg_or_path.endswith(".py"):
        p = Path(pkg_or_path)
        if p.exists():
            return None, [str(p.resolve())]
    spec = importlib.util.find_spec(pkg_or_path)
    if spec and spec.submodule_search_locations:
        return pkg_or_path, list(spec.submodule_search_locations)
    p = Path(pkg_or_path)
    if p.exists():
        return None, [str(p.resolve())]
    raise ModuleNotFoundError(
        f"Cannot locate package or folder: {pkg_or_path!r}"
    )


def _module_name_from_file(pkg_name: str, root: str, file_path: Path) -> str:
    """Compute 'endpoints.views.foo.bar' from root and file path."""
    rel = file_path.relative_to(root)
    dotted = ".".join(rel.with_suffix("").parts)
    return f"{pkg_name}.{dotted}"


def _module_name_from_fs(file_path: Path) -> str:
    """
    Best-effort module name from filesystem relative to CWD.
    Requires CWD (project root) to be on sys.path.
    """
    rel = file_path.relative_to(Path().resolve())
    return ".".join(rel.with_suffix("").parts)


def _import_module_for(
        file_path: Path, pkg_name: Optional[str], root: str
) -> object:
    if pkg_name:
        mod_name = _module_name_from_file(pkg_name, root, file_path)
    else:
        mod_name = _module_name_from_fs(file_path)
    return importlib.import_module(mod_name)


def _iter_page_classes(mod) -> Iterable[Type[HTTPEndpoint]]:
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if issubclass(obj, View) and obj is not View:
            yield obj


def _iter_api_classes(mod) -> Iterable[Type[API]]:
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if issubclass(obj, API) and obj is not API:
            yield obj


def _url_from_file(root: Path, file_path: Path) -> str:
    """
    Map file location to URL:
      root/resumes/index.py -> /resumes
      root/resumes/edit.py  -> /resumes/edit
    """
    rel = file_path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1].lower() == "index":
        parts = parts[:-1]
    url = "/" + "/".join(parts)
    return url or "/"


# ---------- builders ----------

def build_routes_from_pages(pages_dir: str = "endpoints.views") -> List[Route]:
    """
    Scan a package (e.g., 'endpoints.views') or folder ('endpoints/views')
    for Page (HTTPEndpoint) subclasses and create Route entries.
    """
    pkg_name, roots = _resolve_roots(pages_dir)
    routes: List[Route] = []
    seen_paths: set[str] = set()

    for root in roots:
        root_path = Path(root)
        for file_path in root_path.rglob("*.py"):
            if file_path.name == "__init__.py":
                continue
            mod = _import_module_for(file_path, pkg_name, root)
            classes = list(_iter_page_classes(mod))
            if not classes:
                continue
            base_path = _url_from_file(root_path, file_path)
            for cls in classes:
                path = getattr(cls, "path", None) or base_path
                if path in seen_paths and getattr(cls, "path", None) is None:
                    path = f"{base_path}/{cls.__name__.lower()}"
                if path not in seen_paths:
                    routes.append(Route(path, endpoint=cls))
                    seen_paths.add(path)
    return routes


def build_routes_from_apis(api_dir: str = "endpoints.api") -> List[Mount]:
    """
    Scan a package (e.g., 'endpoints.apis') or folder ('endpoints/apis')
    for API subclasses and mount them.
    """
    pkg_name, roots = _resolve_roots(api_dir)
    mounts: List[Mount] = []
    for root in roots:
        root_path = Path(root)
        for file_path in root_path.rglob("*.py"):
            if file_path.name == "__init__.py":
                continue
            mod = _import_module_for(file_path, pkg_name, root)
            classes = list(_iter_api_classes(mod))
            if not classes:
                continue
            for cls in classes:
                mounts.append(cls.build_mount())
    return mounts


def build_file_route() -> Optional[Mount]:
    """
    Mount /static if STATIC_PATH exists. Return None otherwise.
    """
    if STATIC_PATH and Path(STATIC_PATH).exists():
        return Mount(
            "/static", StaticFiles(directory=str(STATIC_PATH)), name="static"
        )
    return None
