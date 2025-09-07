from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from starlette.datastructures import URLPath
from starlette.middleware.sessions import SessionMiddleware
from z8ter.core import Z8ter
from z8ter.config import build_config
from z8ter.errors import register_exception_handlers
from z8ter.vite import vite_script_tag
from z8ter import get_templates
from z8ter.auth.middleware import AuthSessionMiddleware


# ---------------------------
# Builder step specification
# ---------------------------

BuilderFunc = Callable[[Dict[str, Any]], None]


@dataclass
class BuilderStep:
    name: str
    func: BuilderFunc
    requires: List[str] = field(default_factory=list)
    idempotent: bool = False
    kwargs: Dict[str, Any] = field(default_factory=dict)


# ---------------------------
# Small helper utilities
# ---------------------------


def _get_config_value(
        context: dict[str, Any], key: str, default: str | None = None
) -> Any:
    """
    Fetch a config value from context["config"].
    Works if config is a callable (config("KEY")) or a dict-like.
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


def _ensure_services(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonical per-app service registry lives in context['services']
    and is mirrored to app.state.services.
    """
    services = context.setdefault("services", {})
    app: Z8ter = context["app"]
    state = app.starlette_app.state
    if not hasattr(state, "services"):
        state.services = services
    return services


def use_service_builder(context: dict) -> None:
    """
    Register an object as a named service in the app.
    Stored in both context['services'] and app.state.services.
    """
    app: Z8ter = context["app"]
    services: dict[str, object] = context.setdefault("services", {})
    obj = context["obj"]
    replace: bool = context.get("replace", False)
    key = (obj.__class__.__name__).rstrip("_").lower()
    if key in services and not replace:
        raise RuntimeError(
            f"Z8ter: service '{key}' already registered. "
            f"Pass replace=True to override."
        )
    services[key] = obj
    state = app.starlette_app.state
    if not hasattr(state, "services"):
        state.services = services
    state.services[key] = obj


# ---------------------------
# Builder functions (fn(context) -> None)
# ---------------------------

def use_config_builder(context: Dict[str, Any]) -> None:
    envfile = context.get("envfile", ".env")
    config = build_config(env_file=envfile)
    context["config"] = config
    services = _ensure_services(context)
    services["config"] = config


def use_templating_builder(context: Dict[str, Any]) -> None:
    app: Z8ter = context["app"]
    templates = get_templates()

    def _url_for(
            name: str,
            filename: Optional[str] = None,
            **params: Any
    ) -> str:
        if filename is not None:
            params["path"] = filename
        path: URLPath = app.starlette_app.url_path_for(name, **params)
        return str(path)
    templates.env.globals["url_for"] = _url_for
    context["templates"] = templates
    services = _ensure_services(context)
    services["templates"] = templates


def use_vite_builder(context: Dict[str, Any]) -> None:
    templates = context.get("templates")
    if not templates:
        raise RuntimeError(
            "Z8ter: 'vite' requires 'templating'. "
            "Call use_templating() before use_vite()."
        )
    templates.env.globals["vite_script_tag"] = vite_script_tag


def use_errors_builder(context: Dict[str, Any]) -> None:
    app: Z8ter = context["app"]
    register_exception_handlers(app)


def publish_auth_repos_builder(context: dict[str, Any]) -> None:
    app = context["app"]
    services = context.setdefault("services", {})
    session_repo = context["session_repo"]
    user_repo = context["user_repo"]
    for name, repo, methods in [
        ("session_repo", session_repo, ["insert", "revoke", "get_user_id"]),
        ("user_repo", user_repo, ["get_user_by_id"]),
    ]:
        for m in methods:
            if not hasattr(repo, m):
                raise RuntimeError(
                    f"Z8ter: {name} missing required method '{m}'. "
                    f"Provided object: {repo.__class__.__name__}"
                )
    app.starlette_app.state.session_repo = session_repo
    app.starlette_app.state.user_repo = user_repo
    services["session_repo"] = session_repo
    services["user_repo"] = user_repo


def use_app_sessions_builder(context: dict[str, Any]) -> None:
    app = context["app"]
    secret_key = _get_config_value(
        context=context, key="APP_SESSION_KEY"
    )
    secret_key = context.get("secret_key") or secret_key
    if secret_key is None:
        raise TypeError("Secret key cannot be none for using app sessions.")
    app.starlette_app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        session_cookie="z8_app_sess",
        max_age=60*60*24*7,
        same_site="lax"
    )


def use_authentication_builder(context: Dict[str, Any]) -> None:
    app: Z8ter = context["app"]
    if getattr(app.starlette_app, "_z8_auth_added", False):
        return
    app.starlette_app.add_middleware(AuthSessionMiddleware)
    setattr(app.starlette_app, "_z8_auth_added", True)
