from z8ter import TEMPLATES_DIR, VIEWS_DIR, TS_DIR, API_DIR
import argparse

'''
CLI support for the following commands -
    1. z8ter create_page newpage
    2. z8ter new project
    3. z8ter run
    4. z8ter run dev
'''


def set_page_content(page_name_lower, class_name) -> dict:
    content = {}
    content["template_content"] = f"""{{% extends "components/base.jinja" %}}
{{% block content %}}
  <h1>{class_name}</h1>
{{% endblock %}}
"""
    content["view_content"] = f"""from z8ter.page import Page
from starlette.requests import Request
from starlette.responses import Response


class {class_name}(Page):
    async def get(self, request: Request) -> Response:
        return self.render(request, "{page_name_lower}.jinja", {{}})
"""
    content["ts_content"] = (
        f"export default function init{class_name}(): void {{}}"
    )
    return content


def create_page(page_name: str):
    page_name_lower = page_name.lower()
    class_name = page_name.capitalize()
    template_path = TEMPLATES_DIR / f"{page_name_lower}.jinja"
    view_path = VIEWS_DIR / f"{page_name_lower}.py"
    ts_path = TS_DIR / "pages" /f"{page_name_lower}.ts"
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    VIEWS_DIR.mkdir(parents=True, exist_ok=True)
    TS_DIR.mkdir(parents=True, exist_ok=True)
    content = set_page_content(page_name_lower, class_name)
    if not template_path.exists():
        template_path.write_text(content["template_content"], encoding="utf-8")
        print(f"Created template: {template_path}")
    else:
        print(f"Template already exists: {template_path}")
    if not view_path.exists():
        view_path.write_text(content["view_content"], encoding="utf-8")
        print(f"Created view: {view_path}")
    else:
        print(f"View already exists: {view_path}")
    if not ts_path.exists():
        ts_path.write_text(content["ts_content"], encoding="utf-8")
        print(f"Created script: {ts_path}")
    else:
        print(f"Script already exists: {ts_path}")


def create_api(api_name: str):
    api_name_lower = api_name.lower()
    class_name = api_name.capitalize()
    api_path = API_DIR / f"{api_name_lower}.py"
    api_content = f"""from z8ter.api import API
from starlette.requests import Request
from starlette.responses import JSONResponse


class {class_name}(Page):
    @API.endpoint("GET", "/")
    async def get_{class_name}(self, request: Request) -> JSONResponse:
        return JSONResponse({{"message": "Hello from {class_name} API!"}}, 200)
"""
    if not api_path.exists():
        api_path.write_text(api_content, encoding="utf-8")
        print(f"Created template: {api_path}")
    else:
        print(f"Template already exists: {api_path}")


def new_project(project_name: str):
    print("This feature has not been implemented yet.")
    print(f"You can start your project {project_name} by cloning the repo:")
    print("https://github.com/ashesh808/Z8ter")


def run_server(
        mode: str = "prod", app_path: str = "main:app",
        host: str = "127.0.0.1", port: int = 8000
        ):
    import uvicorn
    uvicorn.run(app_path, host=host, port=port, reload=(mode == "dev"))


def main():
    parser = argparse.ArgumentParser(prog="z8", description="Z8ter CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create_page",
                              help="Create a new page (template + view)")
    p_create.add_argument("name",
                          help="Page name (e.g., 'home' or 'app/home')")
    p_new = sub.add_parser("new",
                           help="Create a new Z8ter project")
    p_new.add_argument("project_name",
                       help="Folder name for the new project")
    p_run = sub.add_parser("run", help="Run the app (default: prod)")
    p_run.add_argument("mode", nargs="?", choices=["dev"],
                       help="Use 'dev' for autoreload")
    args = parser.parse_args()
    if args.cmd == "create_page":
        create_page(args.name)
    elif args.cmd == "new":
        new_project(args.project_name)
    elif args.cmd == "run":
        run_server(mode="dev" if args.mode == "dev" else "prod")
    else:
        parser.print_help()
