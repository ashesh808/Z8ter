from __future__ import annotations
from pathlib import Path
import importlib
import inspect
from typing import Callable, Awaitable
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from z8ter.page import Page

# ---------- Helpers


def _url_from_file(pages_root: Path, file_path: Path) -> str:
    """Derive /path from views/pages/.../foo.py (index maps to / or /dir)."""
    rel = file_path.relative_to(pages_root).with_suffix("")  # drop .py
    parts = list(rel.parts)
    if parts[-1] == "index":
        parts = parts[:-1]  # .../index -> ...
    url = "/" + "/".join(parts)
    return url or "/"  # empty means root


def _import_module_for(file_path: Path, package_root: str) -> object:
    """Import module using dotted path built from file location."""
    rel = file_path.with_suffix("").as_posix()
    # e.g., views/pages/blog/index.py -> views.pages.blog.index
    dotted = rel.replace("/", ".")
    if not dotted.startswith(package_root):
        dotted = f"{package_root}.{dotted.split(package_root + '.', 1)[-1]}"
    return importlib.import_module(dotted)


def _find_page_class(mod: object) -> type[Page] | None:
    """Return the first concrete subclass of Page in the module, if any."""
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if issubclass(obj, Page) and obj is not Page:
            return obj
    return None


def _endpoint(
        method: Callable[[Page, Request], Awaitable[Response]], page: Page
        ):
    async def handler(request: Request) -> Response:
        return await method(page, request)
    return handler

# ---------- Public API


def build_routes_from_pages(pages_dir: str = "views") -> list[Route]:
    """
    Discover Page subclasses under views and create Starlette routes
    that call their get()/post() methods.
    """
    routes: list[Route] = []
    pages_root = Path(pages_dir).resolve()
    for file_path in pages_root.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue

        mod = _import_module_for(file_path.relative_to(Path().resolve()),
                                 "views")
        cls = _find_page_class(mod)
        if not cls:
            continue

        page: Page = cls()  # instantiate
        path = getattr(page, "path", None) or _url_from_file(pages_root,
                                                             file_path)

        # GET
        if hasattr(page, "get"):
            routes.append(Route(path, _endpoint(type(page).get, page),
                                methods=["GET"]))

        # POST (optional; base Page returns 405)
        if hasattr(page, "post"):
            routes.append(Route(path, _endpoint(type(page).post, page),
                                methods=["POST"]))

    # Deterministic order (shorter paths first, then alpha) to avoid shadowing
    routes.sort(key=lambda r: (len(r.path), r.path))
    return routes
