from __future__ import annotations
from typing import Any
from collections import deque
from starlette.routing import Route, Mount
from starlette.applications import Starlette
from z8ter.core import Z8ter
from z8ter.route_builders import (
    build_routes_from_pages,
    build_routes_from_apis,
    build_file_route,
)
from z8ter.builders.builder_functions import (
    BuilderStep,
    use_service_builder,
    publish_auth_repos_builder,
    use_authentication_builder,
    use_templating_builder,
    use_vite_builder,
    use_config_builder,
    use_errors_builder,
    use_app_sessions_builder
)


class AppBuilder:
    def __init__(self) -> None:
        self.routes: list[Route] = []
        self.builder_queue: deque[BuilderStep] = deque()

    # ---------- Route utilities

    def add_routes(self, path: str, func) -> None:
        self.routes.append(Route(path, func))

    def _assemble_routes(self) -> list[Route | Mount]:
        routes: list[Route | Mount] = []
        routes += self.routes

        file_mt = build_file_route()
        if file_mt:
            routes.append(file_mt)

        routes += build_routes_from_pages()
        routes += build_routes_from_apis()
        return routes

    # -- Enqueue feature steps (FIFO). kwargs merged into context at build.

    def use_service(self, obj: object, *, replace: bool = False) -> None:
        self.builder_queue.append(BuilderStep(
            name="service",
            func=use_service_builder,
            requires=[],
            idempotent=False,
            kwargs={"obj": obj, "replace": replace},
        ))

    def use_config(self, envfile: str = ".env") -> None:
        self.builder_queue.append(BuilderStep(
            name="config",
            func=use_config_builder,
            requires=[],
            idempotent=True,
            kwargs={"envfile": envfile},
        ))

    def use_templating(self) -> None:
        self.builder_queue.append(BuilderStep(
            name="templating",
            func=use_templating_builder,
            requires=[],
            idempotent=True,
        ))

    def use_vite(self) -> None:
        self.builder_queue.append(BuilderStep(
            name="vite",
            func=use_vite_builder,
            requires=["templating"],
            idempotent=True,
        ))

    def use_auth_repos(
            self, *, session_repo: object, user_repo: object
    ) -> None:
        self.builder_queue.append(BuilderStep(
            name="auth_repos",
            func=publish_auth_repos_builder,
            requires=[],
            idempotent=True,
            kwargs={"session_repo": session_repo, "user_repo": user_repo},
        ))

    def use_app_sessions(
            self, *, secret_key: str | None = None
    ) -> None:
        self.builder_queue.append(BuilderStep(
            name="app_sessions",
            func=use_app_sessions_builder,
            requires=[],
            idempotent=True,
            kwargs={"secret_key": secret_key},
        ))

    def use_authentication(self) -> None:
        self.builder_queue.append(BuilderStep(
            name="auth",
            func=use_authentication_builder,
            requires=["auth_repos"],
            idempotent=True,
        ))

    def use_errors(self) -> None:
        self.builder_queue.append(BuilderStep(
            name="errors",
            func=use_errors_builder,
            requires=[],
            idempotent=True,
        ))

    # ---------- Build

    def build(self, debug: bool = True) -> Z8ter:
        starlette_app = Starlette(
            debug=debug,
            routes=self._assemble_routes(),
        )
        app = Z8ter(
            debug=debug,
            starlette_app=starlette_app,
        )
        context: dict[str, Any] = {
            "app": app,
            "services": {},
            "debug": debug,
        }
        applied: set[str] = set()
        while self.builder_queue:
            step = self.builder_queue.popleft()
            if step.name in applied:
                if step.idempotent:
                    continue
                raise RuntimeError(
                    f"Z8ter: step '{step.name}' scheduled more "
                    "than once but is not idempotent."
                )
            missing = [r for r in step.requires if r not in applied]
            if missing:
                need = ", ".join(missing)
                hint = ""
                if "auth_repos" in missing and step.name == "auth":
                    hint = " → "
                    "Call use_auth_repos(session_repo=..., user_repo=...) "
                    "before use_authentication()."
                raise RuntimeError(
                    f"Z8ter: step '{step.name}' requires [{need}].{hint}"
                )
            if step.kwargs:
                context.update(step.kwargs)
            step.func(context)
            applied.add(step.name)
        if debug:
            print(
                f"[Z8ter] Build complete. Applied steps: {', '.join(applied)}"
            )
        return app
