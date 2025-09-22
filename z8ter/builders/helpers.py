"""Helper functions used by builder_functions and app_builder."""

from typing import Any

from z8ter.core import Z8ter


def get_config_value(
    context: dict[str, Any], key: str, default: str | None = None
) -> Any:
    """Fetch a config value from `context["config"]`.

    Supports both callable config accessors (e.g., `config("KEY")`) and
    mapping-like objects (e.g., `dict`).

    Args:
        context: Shared build context.
        key: Configuration key to read.
        default: Fallback value if missing or on error.

    Returns:
        The resolved value or `default` if unavailable.

    """
    cfg = context.get("config")
    if cfg is None:
        return default
    if callable(cfg):
        try:
            return cfg(key)
        except Exception:
            return default
    try:
        return cfg.get(key, default)
    except AttributeError:
        try:
            return cfg[key]
        except Exception:
            return default


def ensure_services(context: dict[str, Any]) -> dict[str, Any]:
    """Ensure a canonical service registry exists and is mirrored to app state.

    Side effects:
        - Creates/returns `context["services"]`.
        - Mirrors the dict to `app.starlette_app.state.services` if absent.

    Args:
        context: Shared build context.

    Returns:
        The service registry dict.

    """
    services = context.setdefault("services", {})
    app: Z8ter = context["app"]
    state = app.starlette_app.state
    if not hasattr(state, "services"):
        state.services = services
    return services


def service_key(obj) -> str:
    """Return a stable service key for DI service registration.

    Prefers an explicit `name` attribute; falls back to the class name.

    Args:
        obj: Service instance being registered.

    Returns:
        str: The key under which the service is stored in context["services"].

    """
    return getattr(obj, "name", obj.__class__.__name__)
