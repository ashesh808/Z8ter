from __future__ import annotations

from starlette.testclient import TestClient

from z8ter.builders.app_builder import AppBuilder
from z8ter.endpoints.view import View


class Derived(View):
    pass


def test_view_derives_page_id_from_module_name() -> None:
    assert Derived._page_id == Derived.__module__


def test_view_render_injects_context_and_content() -> None:
    builder = AppBuilder()
    builder.use_config(".env")
    builder.use_templating()
    builder.use_vite()
    builder.use_errors()
    app = builder.build(debug=False)

    client = TestClient(app.starlette_app)
    response = client.get("/")

    assert response.status_code == 200
    assert "Z8ter" in response.text
    assert response.context["page_id"] == "index"
    assert "page_content" in response.context
