from __future__ import annotations
from pathlib import Path
import importlib
from typing import Iterable, Type
from starlette.routing import Route, Mount
from starlette.endpoints import HTTPEndpoint
from z8ter.api import API


def _import_module_for(rel_path: Path, package_root: str) -> object:
    mod_name = str(rel_path.with_suffix("")).replace(
        "/", ".").replace("\\", ".")
    if mod_name.startswith(f"{package_root}."):
        full_name = mod_name
    else:
        full_name = f"{package_root}.{mod_name}"
    return importlib.import_module(full_name)


def _iter_page_classes(mod) -> Iterable[Type[HTTPEndpoint]]:
    from .page import Page
    for obj in vars(mod).values():
        if isinstance(obj, type) and issubclass(obj, Page) and obj is not Page:
            yield obj


def _iter_api_classes(mod) -> Iterable[Type[API]]:
    from .api import API
    for obj in vars(mod).values():
        if isinstance(obj, type) and issubclass(obj, API) and obj is not API:
            yield obj


def _url_from_file(pages_root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(pages_root).with_suffix("")
    parts = rel.parts
    url = "/" + "/".join(parts)
    if url.endswith("/index"):
        url = url[:-len("/index")] or "/"
    return url or "/"


def build_routes_from_pages(pages_dir: str = "views") -> list[Route]:
    routes: list[Route] = []
    pages_root = Path(pages_dir).resolve()
    seen_paths: set[str] = set()
    for file_path in pages_root.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue
        rel_to_cwd = file_path.relative_to(Path().resolve())
        mod = _import_module_for(rel_to_cwd, pages_dir)
        classes = list(_iter_page_classes(mod))
        if not classes:
            continue
        base_path = _url_from_file(pages_root, file_path)
        for cls in classes:
            path = getattr(cls, "path", None) or base_path
            if path in seen_paths and getattr(cls, "path", None) is None:
                path = f"{base_path}/{cls.__name__.lower()}"
            if path not in seen_paths:
                routes.append(Route(path, cls))
                seen_paths.add(path)
    return routes


def build_routes_from_apis(api_dir: str = "api") -> list[Mount]:
    routes: list[Mount] = []
    pages_root = Path(api_dir).resolve()
    for file_path in pages_root.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue
        rel_to_cwd = file_path.relative_to(Path().resolve())
        mod = _import_module_for(rel_to_cwd, api_dir)
        classes = list(_iter_api_classes(mod))
        if not classes:
            continue
        for cls in classes:
            routes.append(cls.build_mount())
    return routes


def build_favicon_route(api_dir: str = "static/favicon") -> list[Mount]:
    routes: list[Mount] = []
    pages_root = Path(api_dir).resolve()
    for file_path in pages_root.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue
        rel_to_cwd = file_path.relative_to(Path().resolve())
        mod = _import_module_for(rel_to_cwd, api_dir)
        classes = list(_iter_api_classes(mod))
        if not classes:
            continue
        for cls in classes:
            routes.append(cls.build_mount())
    return routes
