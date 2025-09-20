"""Endpoint utilities for rendering templates and loading page content.

This module provides helpers to:
  - Render a Jinja template into a Starlette `Response`.
  - Load structured YAML content for a page, keyed by `page_id`.

Conventions:
  - Content files live under BASE_DIR/content/{page_id}.yaml.
  - Templates are resolved via the app's Jinja2 environment.
"""

from __future__ import annotations

import pathlib
from typing import Any

import yaml
from starlette.templating import Jinja2Templates

from z8ter import BASE_DIR, get_templates
from z8ter.responses import Response

# Default path for user-facing page content.
contents_path = BASE_DIR / "content"


def render(template_name: str, context: dict[str, Any] | None = None) -> Response:
    """Render a Jinja template into a Starlette `TemplateResponse`.

    Args:
        template_name: Path to the Jinja template, relative to templates dir.
        context: Template context variables. May be None.

    Returns:
        Response: A Starlette TemplateResponse object.

    Notes:
        - Unlike Starlette, this wrapper does not automatically inject `request`
          into the context. You may want to add it in higher-level view helpers.
        - Response type is framework-specific but generally behaves like ASGI.

    """
    templates: Jinja2Templates = get_templates()
    return templates.TemplateResponse(template_name, context)


def load_content(page_id: str) -> dict[str, Any]:
    """Load YAML page content for a given page id.

    Args:
        page_id: Dot- or slash-based identifier (e.g., "about" or "app.home").
            Dots are converted to slashes before resolving the content path.

    Returns:
        dict[str, Any]: A dict containing {"page_content": <parsed_yaml>}.

    Raises:
        FileNotFoundError: If the expected YAML file does not exist.
        yaml.YAMLError: If the YAML content is malformed.

    Example:
        >>> load_content("about")
        {"page_content": {"title": "About Us", "body": "..."}}

    """
    content_yaml = page_id.replace(".", "/") + ".yaml"
    content_path = contents_path / content_yaml
    ctx = yaml.safe_load(pathlib.Path(content_path).read_text())
    return {"page_content": ctx}
