from z8ter import TEMPLATES_DIR, VIEWS_DIR
import sys

'''
CLI support for the following commands -
    1. z8ter create_page newpage
    2. z8ter new project
    3. z8ter run
    4. z8ter run dev
'''


def create_page(page_name: str):
    # Normalize names
    page_name_lower = page_name.lower()
    class_name = page_name.capitalize()

    # File paths
    template_path = TEMPLATES_DIR / f"{page_name_lower}.jinja"
    view_path = VIEWS_DIR / f"{page_name_lower}.py"

    # Ensure directories exist
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    VIEWS_DIR.mkdir(parents=True, exist_ok=True)

    # Template content
    template_content = f"""{{% extends "components/base.jinja" %}}
{{% block content %}}
  <h1>{page_name.capitalize()}</h1>
{{% endblock %}}
"""

    # View content
    view_content = f"""from z8ter.page import Page
from starlette.requests import Request
from starlette.responses import Response


class {class_name}(Page):
    async def get(self, request: Request) -> Response:
        return self.render(request, "{page_name_lower}.jinja", {{}})
"""

    # Write files (skip if exists)
    if not template_path.exists():
        template_path.write_text(template_content, encoding="utf-8")
        print(f"Created template: {template_path}")
    else:
        print(f"Template already exists: {template_path}")

    if not view_path.exists():
        view_path.write_text(view_content, encoding="utf-8")
        print(f"Created view: {view_path}")
    else:
        print(f"View already exists: {view_path}")


def run():
    if len(sys.argv) != 3 or sys.argv[1] != "create_page":
        print("Usage: z8 create_page <page_name>")
        sys.exit(1)
    page_name = sys.argv[2]
    create_page(page_name)
