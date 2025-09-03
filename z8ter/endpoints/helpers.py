from __future__ import annotations
from typing import Any
import yaml
import pathlib
from starlette.templating import Jinja2Templates
from z8ter.responses import Response
from z8ter import get_templates
from z8ter import BASE_DIR

contents_path = BASE_DIR / "content"


def render(
        template_name: str,
        context: dict[str, Any] | None = None
) -> Response:
    templates: Jinja2Templates = get_templates()
    return templates.TemplateResponse(template_name, context)


def load_content(page_id: str) -> dict:
    content_yaml = page_id.replace('.', '/') + ".yaml"
    content_path = contents_path / content_yaml
    ctx = yaml.safe_load(
        pathlib.Path(content_path).read_text()
    )
    return {"page_content": ctx}
