from __future__ import annotations

import pytest
from starlette.routing import Route

from z8ter.builders.app_builder import AppBuilder


def _collect_paths(app) -> set[str]:
    paths: set[str] = set()
    for route in app.starlette_app.routes:
        if isinstance(route, Route):
            paths.add(route.path)
    return paths


def test_app_builder_constructs_application() -> None:
    builder = AppBuilder()
    builder.use_config(".env")
    builder.use_templating()
    builder.use_templating()  # idempotent
    builder.use_vite()
    builder.use_errors()
    app = builder.build(debug=False)

    assert _collect_paths(app)  # at least one route discovered (index page)
    assert "/" in _collect_paths(app)


def test_app_builder_enforces_dependencies() -> None:
    builder = AppBuilder()
    builder.use_authentication()

    with pytest.raises(RuntimeError) as exc:
        builder.build(debug=False)

    assert "requires [auth_repos]" in str(exc.value)


def test_app_builder_rejects_duplicate_non_idempotent_steps() -> None:
    builder = AppBuilder()

    from z8ter.builders.builder_functions import use_service_builder
    from z8ter.builders.builder_step import BuilderStep

    builder.builder_queue.append(
        BuilderStep(
            name="custom",
            func=use_service_builder,
            requires=[],
            idempotent=False,
            kwargs={"obj": object()},
        )
    )
    builder.builder_queue.append(
        BuilderStep(
            name="custom",
            func=use_service_builder,
            requires=[],
            idempotent=False,
            kwargs={"obj": object()},
        )
    )

    with pytest.raises(RuntimeError) as exc:
        builder.build(debug=False)

    assert "scheduled more than once" in str(exc.value)
