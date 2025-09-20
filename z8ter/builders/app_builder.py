"""Application builder for Z8ter.

This module assembles a Starlette app plus Z8ter conveniences by queuing
discrete "builder steps" (config, templating, vite, auth, errors, etc.) and
executing them in dependency order. It also collects routes from file-based
pages and API classes.

Key ideas:
- FIFO queue of `BuilderStep`s with `requires` edges for dependency safety.
- Idempotent steps are skipped if scheduled more than once.
- Services are published into a shared `context` (e.g., config, repos).
- Routes are composed from explicit additions plus file/page/api discovery.

Public surface:
- `AppBuilder`: queue feature steps and produce a configured `Z8ter` app.

Notes:
- Keep steps lightweight and deterministic. Expensive work should be deferred
  to runtime or a separate build step.

"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import Any

from starlette.applications import Starlette
from starlette.routing import Mount, Route

from z8ter.builders.builder_functions import (
    BuilderStep,
    publish_auth_repos_builder,
    use_app_sessions_builder,
    use_authentication_builder,
    use_config_builder,
    use_errors_builder,
    use_service_builder,
    use_templating_builder,
    use_vite_builder,
)
from z8ter.core import Z8ter
from z8ter.route_builders import (
    build_file_route,
    build_routes_from_apis,
    build_routes_from_pages,
)


def _service_key(obj) -> str:
    """Return a stable service key for DI service registration.

    Prefers an explicit `name` attribute; falls back to the class name.

    Args:
        obj: Service instance being registered.

    Returns:
        str: The key under which the service is stored in context["services"].

    """
    return getattr(obj, "name", obj.__class__.__name__)


class AppBuilder:
    """Composable application builder.

    Queue builder steps (config, templating, auth, etc.), optionally add custom
    routes, then call `build()` to produce a ready-to-run `Z8ter` app.

    Attributes:
        routes: Explicit routes added via `add_routes`.
        builder_queue: FIFO queue of `BuilderStep` instances to apply.

    """

    def __init__(self) -> None:
        """Initialize an empty builder."""
        self.routes: list[Route] = []
        self.builder_queue: deque[BuilderStep] = deque()

    # ---------- Route utilities

    def add_routes(self, path: str, func: Callable[..., Any]) -> None:
        """Add a single Starlette route.

        Args:
            path: URL path (e.g., "/health").
            func: ASGI handler or function compatible with Starlette `Route`.

        Notes:
            - This is a thin helper; more complex mounts should be added via the
              route builders or Starlette `Mount`.

        """
        self.routes.append(Route(path, func))

    def _assemble_routes(self) -> list[Route | Mount]:
        """Collect built-in and discovered routes into a single list.

        Returns:
            A list of Starlette `Route`/`Mount` objects to pass to Starlette.

        """
        routes: list[Route | Mount] = []
        routes += self.routes

        # Mount static/file route if available (may be None in certain configs).
        file_mt = build_file_route()
        if file_mt:
            routes.append(file_mt)

        # Add SSR page routes and API routes discovered from the filesystem.
        routes += build_routes_from_pages()
        routes += build_routes_from_apis()
        return routes

    # -- Enqueue feature steps (FIFO). kwargs merged into context at build.

    def use_service(self, obj: object, *, replace: bool = False) -> None:
        """Publish a service instance into the build context.

        Services are accessible at `context["services"][key]` where `key` comes
        from `_service_key(obj)`.

        Args:
            obj: Service instance to publish.
            replace: If True, replace existing service with same key.

        Notes:
            - Marked idempotent. Re-adding the same named service has no effect
              unless `replace=True`.

        """
        key = _service_key(obj)
        self.builder_queue.append(
            BuilderStep(
                name=f"service:{key}",
                func=use_service_builder,
                requires=[],
                idempotent=True,
                kwargs={"obj": obj, "replace": replace},
            )
        )

    def use_config(self, envfile: str = ".env") -> None:
        """Load configuration and publish a `config` accessor service.

        Args:
            envfile: Path to an `.env` file to load (optional).

        """
        self.builder_queue.append(
            BuilderStep(
                name="config",
                func=use_config_builder,
                requires=[],
                idempotent=True,
                kwargs={"envfile": envfile},
            )
        )

    def use_templating(self) -> None:
        """Enable Jinja templating and template environment."""
        self.builder_queue.append(
            BuilderStep(
                name="templating",
                func=use_templating_builder,
                requires=[],
                idempotent=True,
            )
        )

    def use_vite(self) -> None:
        """Wire Vite dev server/build output for assets.

        Requires:
            - `templating` step to have been applied.
        """
        self.builder_queue.append(
            BuilderStep(
                name="vite",
                func=use_vite_builder,
                requires=["templating"],
                idempotent=True,
            )
        )

    def use_auth_repos(self, *, session_repo: object, user_repo: object) -> None:
        """Publish authentication repositories (session + user).

        Args:
            session_repo: Implementation of `SessionRepo`.
            user_repo: Implementation of `UserRepo`.

        """
        self.builder_queue.append(
            BuilderStep(
                name="auth_repos",
                func=publish_auth_repos_builder,
                requires=[],
                idempotent=True,
                kwargs={"session_repo": session_repo, "user_repo": user_repo},
            )
        )

    def use_app_sessions(self, *, secret_key: str | None = None) -> None:
        """Enable application-level session cookies (non-auth).

        Args:
            secret_key: Optional signing/encryption key for app sessions. If not
                provided, a framework default may be used (discouraged for prod).

        """
        self.builder_queue.append(
            BuilderStep(
                name="app_sessions",
                func=use_app_sessions_builder,
                requires=[],
                idempotent=True,
                kwargs={"secret_key": secret_key},
            )
        )

    def use_authentication(self) -> None:
        """Enable authentication (middleware, guards, helpers).

        Requires:
            - `auth_repos` to have been published.
        """
        self.builder_queue.append(
            BuilderStep(
                name="auth",
                func=use_authentication_builder,
                requires=["auth_repos"],
                idempotent=True,
            )
        )

    def use_errors(self) -> None:
        """Install error handlers (HTTPException views, fallbacks)."""
        self.builder_queue.append(
            BuilderStep(
                name="errors",
                func=use_errors_builder,
                requires=[],
                idempotent=True,
            )
        )

    # ---------- Build

    def build(self, debug: bool = True) -> Z8ter:
        """Construct the Starlette app and apply all queued builder steps.

        Args:
            debug: Enable Starlette/Z8ter debug behavior.

        Returns:
            Z8ter: A configured Z8ter application ready to run.

        Raises:
            RuntimeError: If a non-idempotent step is scheduled more than once or
                if required steps are missing when a step executes.

        """
        starlette_app = Starlette(
            debug=debug,
            routes=self._assemble_routes(),
        )
        app = Z8ter(
            debug=debug,
            starlette_app=starlette_app,
        )

        # Shared context for all builder steps. Steps may mutate it in place.
        context: dict[str, Any] = {
            "app": app,
            "services": {},
            "debug": debug,
        }

        applied: set[str] = set()

        while self.builder_queue:
            step = self.builder_queue.popleft()

            # Prevent duplicate application of non-idempotent steps.
            if step.name in applied:
                if step.idempotent:
                    continue
                raise RuntimeError(
                    f"Z8ter: step '{step.name}' scheduled more than once but is "
                    "not idempotent."
                )

            # Enforce dependencies.
            missing = [r for r in step.requires if r not in applied]
            if missing:
                need = ", ".join(missing)
                hint = ""
                if "auth_repos" in missing and step.name == "auth":
                    # FIX: Previously, string literals were separated across lines
                    # without parentheses, so `hint` stayed as " → " only.
                    hint = (
                        " → Call use_auth_repos(session_repo=..., user_repo=...) "
                        "before use_authentication()."
                    )
                raise RuntimeError(
                    f"Z8ter: step '{step.name}' requires [{need}].{hint}"
                )

            # Merge step kwargs into context (last writer wins).
            if step.kwargs:
                context.update(step.kwargs)

            # Execute the builder function with the shared context.
            step.func(context)
            applied.add(step.name)

        if debug:
            print(f"[Z8ter] Build complete. Applied steps: {', '.join(applied)}")

        return app
