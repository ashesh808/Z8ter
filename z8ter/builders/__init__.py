"""Z8ter app builders.

This package provides the composable build pipeline used to assemble a Z8ter
application (routes, services, middleware, templating, assets, etc.).

Public modules:
- `app_builder`: High-level orchestration (`AppBuilder`).
- `builder_functions`: Step spec (`BuilderStep`) and concrete `use_*_builder`
  functions for config, templating, vite, errors, auth repos, and app sessions.

Typical usage:
    from z8ter.builders import AppBuilder

    b = AppBuilder()
    b.use_config(".env")
    b.use_templating()
    b.use_vite()
    b.use_errors()
    b.use_auth_repos(session_repo=..., user_repo=...)
    b.use_authentication()
    app = b.build(debug=True)

Design notes:
- Steps are applied in FIFO order with dependency checks (`requires`).
- Idempotent steps may be scheduled multiple times safely.
- Services published by steps are available at `app.starlette_app.state.services`.
"""

from .app_builder import AppBuilder
from .builder_functions import (
    publish_auth_repos_builder,
    use_app_sessions_builder,
    use_authentication_builder,
    use_config_builder,
    use_errors_builder,
    use_service_builder,
    use_templating_builder,
    use_vite_builder,
)
from .builder_step import BuilderStep

__all__ = [
    "AppBuilder",
    "BuilderStep",
    "use_service_builder",
    "use_config_builder",
    "use_templating_builder",
    "use_vite_builder",
    "use_errors_builder",
    "publish_auth_repos_builder",
    "use_app_sessions_builder",
    "use_authentication_builder",
]
