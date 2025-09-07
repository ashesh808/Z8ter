import json
import os
from pathlib import Path
from markupsafe import Markup

DIST = Path("static/js/.vite")
VITE_DEV_SERVER = os.getenv("VITE_DEV_SERVER", "").rstrip("/")
_manifest_cache: dict[str, object] | None = None
_manifest_mtime: float | None = None


def _load_manifest() -> dict:
    global _manifest_cache, _manifest_mtime
    path = DIST / "manifest.json"
    stat = path.stat()
    if _manifest_cache is None or _manifest_mtime != stat.st_mtime:
        _manifest_cache = json.loads(path.read_text())
        _manifest_mtime = stat.st_mtime
    return _manifest_cache  # type: ignore[return-value]


def vite_script_tag(entry: str) -> Markup:
    """
    Return <script> (and optional <link rel=modulepreload>) tags.
    - Dev: if VITE_DEV_SERVER is set, load from dev server (no manifest).
    - Prod: read manifest.json, auto-reload when the file changes.
    """
    # DEV SERVER MODE -------------------------------------------------
    if VITE_DEV_SERVER:
        return Markup(
            f'<script type="module" src="{VITE_DEV_SERVER}/{entry}"></script>'
        )
    # BUILD/MANIFEST MODE --------------------------------------------
    manifest = _load_manifest()
    if entry not in manifest:
        available = ", ".join(sorted(manifest.keys()))
        raise KeyError(
            f"Vite entry '{entry}' not found in manifest."
            f"Available: {available}"
            )
    item = manifest[entry]
    tags: list[str] = [
        f'<script type="module" src="/static/js/{item["file"]}"></script>'
    ]
    for imp in item.get("imports", []):
        dep = manifest.get(imp)
        if dep and "file" in dep:
            tags.append(
                f'<link rel="modulepreload" href="/static/js/{dep["file"]}">')
    for css in item.get("css", []):
        tags.append(f'<link rel="stylesheet" href="/static/js/{css}">')
    return Markup("\n".join(tags))
