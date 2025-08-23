# Z8ter.py

**Z8ter** is a lightweight, Laravel-inspired full-stack Python web framework built on [Starlette], designed for rapid development with tight integration between backend logic and frontend templates—plus small client-side “islands” where they make sense.

---

## ✨ Features (Current)

### 1) File-Based Views (SSR)
- Files under `views/` become routes automatically.
- Each view pairs Python logic with a Jinja template in `templates/`.
- A stable `page_id` (derived from `views/` path) is injected into templates and used by the frontend loader to hydrate per-page JS.

### 2) Jinja2 Templating
- Template inheritance with `{% extends %}` / `{% block %}`.
- Templates live in `templates/` (default extension: `.jinja`).

### 3) Small CSR “Islands”
- A tiny client router lazy-loads `/static/js/pages/<page_id>.js` and runs its default export.
- Great for interactive bits (theme toggles, pings, clipboard, etc.) without going full SPA.

### 4) Decorator-Driven APIs
- Classes under `api/` subclass `API` and register endpoints with a decorator.
- Each class mounts under `/api/<id>` (derived from module path).

> Example shape (conceptual):
> ```
> api/hello.py      →  /api/hello
> views/about.py    →  /about
> templates/about.jinja + static/js/pages/about.js (island)
> ```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+ and `pip`
- Node 18+ and `npm`

### Install & Run (dev)
```bash
# 1) Python deps (in a venv)
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # or: pip install -e .

# 2) Frontend deps
npm install

# 3) Dev server(s)
npm run dev
````

> `npm run dev` runs the dev workflow (backend + assets). Check the terminal for the local URL.

---

## 📁 Project Structure

```
.
├─ api/                     # API classes (@API.endpoint)
│  └─ hello.py
├─ views/                   # File-based pages (SSR)
│  └─ index.py
├─ templates/               # Jinja templates
│  ├─ base.jinja
│  └─ index.jinja
├─ static/
│  └─ js/
│     └─ pages/             # Per-page islands: about.js, app/home.js, ...
│        └─ common.js
├─ z8ter/                   # Framework core (Page, API, router)
└─ main.py                  # App entrypoint
```

---

## 🧩 Usage Examples

### View + Template (SSR)

```jinja
{# templates/index.jinja #}
{% extends "base.jinja" %}
{% block content %}
  <h1>{{ title }}</h1>
  <div id="api-response"></div>
{% endblock %}
```

### Client Island (runs when `page_id` matches)

```ts
// static/js/pages/common.ts (or a specific page module)
export default async function init() {
  // hydrate interactive bits, fetch data, etc.
}
```

### Minimal API Class

```python
# api/hello.py
from z8ter.api import API

class Hello(API):
    @API.endpoint("GET", "/hello")
    async def hello(self, request):
        return {"ok": True, "message": "Hello from Z8ter"}
```

---

## 🛣️ Planned

* **CLI scaffolding**: `z8 new`, `z8 dev`, `z8 create_page <name>`
* **Auth scaffolding**: login/register/logout + session helpers
* **Stripe integration**: pricing page, checkout routes, webhooks
* **DB adapters**: SQLite default, Postgres option
* **HTMX + Tailwind/DaisyUI** polish out of the box

---

## 🧠 Philosophy

* Conventions over configuration
* SSR-first with tiny CSR islands
* Small surface area; sharp, pragmatic tools
