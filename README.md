# Z8ter

**Z8ter** is a lightweight full-stack async Python web framework built on Starlette designed for rapid development without compromising on UX.

---
> ⚠️ **Status: Public Alpha** – Currently, Z8ter is **not recommended for production**. APIs may change without notice. 

## Quickstart

```bash
z8 new myapp
cd myapp
python3 -m venv venv
source venv/source/bin
pip3 install -r requirements.txt
z8 run dev
```

---

## Features

1. **File-based routing** – Views in `views/` map to routes automatically, each paired with a Jinja template and optional API.
2. **Clear server/client split** – Server-side rendering by default, with optional client-side “islands” (`static/js/pages/<page_id>.js`) for interactivity.
3. **Simple APIs** – Define API classes with decorators; auto-mounted under `/api/<name>`.
4. **Auth & guards** – Session middleware, Argon2 password hashing, and route decorators like `@login_required`.
5. **Builder setup** – `AppBuilder` manages config, templating, vite, auth, and errors in a consistent order.
6. **CLI tooling** – Scaffold projects, pages, and APIs with `z8 new`, `z8 create_page`, `z8 create_api`; run with `z8 run dev`.

---

## Installation

```bash
pip install z8ter
```

---

## Authentication Example

```python
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

## License

MIT © [Ashesh Nepal](https://linkedin.com/in/ashesh808)
