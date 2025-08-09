from starlette.responses import HTMLResponse, Response
from starlette.routing import Route
from pathlib import Path


def catch_all_route(views_dir: str = "views") -> list[Route]:
    def dynamic_view_handler(request):
        path = request.url.path.lstrip("/") or "index"
        view_path = Path(views_dir) / (path + ".html")
        print(f"🛠 Looking for: {view_path}")
        if view_path.exists():
            return HTMLResponse(view_path.read_text(encoding="utf-8"))
        return Response("Page not found", status_code=404)
    routes = [Route("/{path:path}", dynamic_view_handler)]
    return routes


def build_routes_from_views(views_dir: str = "views") -> list[Route]:
    routes = []
    view_files = Path(views_dir).rglob("*.html")
    for file_path in view_files:
        route_name = file_path.relative_to(
            views_dir
            ).with_suffix(
                ""
                ).as_posix()
        route_path = "/" + str(route_name)
        if route_path == "/index":
            route_path = "/"

        def handler_factory(fp):
            def handler(request):
                return HTMLResponse(open(fp, encoding="utf-8").read())
            return handler

        routes.append(Route(route_path, handler_factory(str(file_path))))

    return routes
