# Z8ter

**Z8ter** is a lightweight, Laravel-inspired full-stack Python web framework built on \[Starlette]. It’s designed for **rapid SaaS development** with a sharp, minimal surface area: server-side rendering by default, plus small client-side islands when you need them.

---

## Features

- **File-based Views (SSR-first)**

  - Files in `views/` become routes automatically.
  - Each view pairs Python logic with a Jinja template in `templates/`.
  - A stable `page_id` is injected into templates for per-page JS hydration.

- **Jinja2 Templating**

  - Full template inheritance with `{% extends %}` / `{% block %}`.
  - Globals like `url_for()` and `vite_script_tag()` wired automatically.

- **Small CSR “Islands”**

  - Drop a `static/js/pages/<page_id>.js` file and it’s lazy-loaded automatically.
  - Perfect for interactive sprinkles (toggles, pings, clipboard).

- **Decorator-driven APIs**

  - Define APIs with `class MyApi(API)` and decorate methods with `@API.endpoint`.
  - Auto-mounted under `/api/<name>`.

- **Authentication & Guards**

  - Session middleware with pluggable `SessionRepo` and `UserRepo`.
  - Built-in password hashing (Argon2).
  - Route decorators: `@login_required`, `@skip_if_authenticated`.
  - Extensible guard system (coming soon): onboarding checks, RBAC, SSO.

- **Builder Pattern for App Setup**

  - `AppBuilder` queues setup steps (config, templating, vite, auth, errors).
  - Consistent, idempotent initialization with clear dependency order.

- **CLI Scaffolding**

  - `z8 new` → scaffold a new project.
  - `z8 create_page <name>` → add a view + template + island.
  - `z8 create_api <name>` → add an API class.
  - `z8 run [dev|prod|LAN|WAN]` → run the app with Uvicorn.

- **DX & Debugging**

  - Rich-powered logging with filtered cancelled errors.
  - Clear error responses in JSON by default.
  - Auto-reloading dev server with Vite integration.

---

## Installation

```bash
pip install z8ter
```

---

## Quickstart

```bash
# 1. Create a new project
z8 new myapp
cd myapp

# 2. Create a page
z8 create_page home

# 3. Run the dev server with auto-reload
z8 run dev
```

Your project will have:

```
myapp/
├─ api/                # API classes
├─ views/              # File-based SSR pages
├─ templates/          # Jinja templates
├─ static/js/pages/    # Client islands
├─ content/            # Page-specific YAML context
└─ main.py             # Entrypoint
```

---

## Authentication Example

```python
# views/dashboard.py
from z8ter.endpoints.view import View
from z8ter.auth.guards import login_required

class Dashboard(View):
    @login_required
    async def get(self, request):
        return self.render(request, "dashboard.jinja")
```

---

## AppBuilder Example

```python
from z8ter.builders.app_builder import AppBuilder
from myapp.repos import MySessionRepo, MyUserRepo

builder = AppBuilder()
builder.use_config(".env")
builder.use_templating()
builder.use_vite()
builder.use_app_sessions(secret_key="supersecret")
builder.use_auth_repos(session_repo=MySessionRepo(), user_repo=MyUserRepo())
builder.use_authentication()
builder.use_errors()

app = builder.build(debug=True)
```

---

## Modules Overview

- `z8ter.auth` → Contracts, crypto (Argon2), guards, session middleware/manager.
- `z8ter.builders` → AppBuilder + builder functions for config, templating, vite, auth, errors.
- `z8ter.cli` → Project scaffolding, page/api generators, run server.
- `z8ter.endpoints` → Base `API` and `View` classes, render/content helpers.
- `z8ter.route_builders` → Route discovery from filesystem and static files.
- `z8ter.responses` / `z8ter.requests` → Thin wrappers around Starlette’s core.
- `z8ter.logging_utils` → Rich logging config with CancelledError suppression.
- `z8ter.errors` → Centralized HTTP + 500 error handlers.
- `z8ter.vite` → Dev/prod script tag helper with manifest reloads.
- `z8ter.config` → Starlette config loader, prepopulated with `BASE_DIR`.
- `z8ter.core` → The `Z8ter` ASGI wrapper around Starlette.

---

## Roadmap

- [ ] **SSO support** (Google, GitHub, LinkedIn).
- [ ] **Guard system** (onboarding, RBAC, prefix-based).
- [ ] **Stripe integration** (`z8 stripe_setup`).
- [ ] **Docker builder** (`z8 build_docker`).
- [ ] **Background tasks** (Redis/RQ).
- [ ] **Admin dashboard generator**.
- [ ] **Plugin system for reusable apps**.

---

## Philosophy

- **Conventions over configuration**: sensible defaults, minimal setup.
- **SSR-first**: HTML-first rendering with small client-side islands.
- **Composable**: builders, guards, repos are pluggable.
- **SaaS-ready**: auth, billing, and multi-tenancy are first-class citizens.

---

## License

MIT © [Ashesh Nepal](https://linkedin.com/in/ashesh808)
