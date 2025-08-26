import json
from pathlib import Path
from markupsafe import Markup

DIST = Path("static/js/dist/.vite")
_manifest = None


def vite_script_tag(entry: str) -> Markup:
    global _manifest
    if _manifest is None:
        path = DIST / "manifest.json"
        _manifest = json.loads(path.read_text())
    item = _manifest[entry]
    tags = [
        f'<script type="module" src="/static/js/dist/{item["file"]}"></script>'
        ]
    for imp in item.get("imports", []):
        tags.append(f'<link rel="modulepreload" href="/static/js/dist/{imp}">')
    return Markup("\n".join(tags))
