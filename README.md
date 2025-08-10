# Z8ter.py

**Z8ter** is a lightweight, Laravel-inspired full-stack Python web framework built on [Starlette](https://www.starlette.io/), designed for rapid development with tight integration between backend logic and frontend templates.

## ✨ Features (Current)

### 1. File-Based Routing
- Pages in the `views/` folder are automatically routed based on file name.
- Example: `views/about.py` → `/about` route.
- Per-page logic with `.py` and `.jinja` template pairing.

### 2. Jinja2 Templating
- Integrated with Starlette’s `Jinja2Templates`.
- Template inheritance with `{% extends %}` and `{% block %}`.
- Templates stored in `templates/` (default extension: `.jinja`).

Example:
```jinja
{% extends "components/base.jinja" %}
{% block content %}
  <h1>{{ title }}</h1>
{% endblock %}
````

### 3. CLI Tooling

* **`z8 create_page <name>`** — scaffolds a `.jinja` template and `.py` page class.
* Generates:

  ```
  templates/<name>.jinja
  views/<name>.py
  ```
* Template includes a basic `<h1>` with the page title.
* Page class renders the template via `Page.render()`.

Example:

```bash
z8 create_page about
```

Output:

```
✅ Created template: templates/about.jinja
✅ Created view: views/about.py
```

---

## 🚧 Planned Features

* **Auth Scaffolding**

  * `z8 create_auth` → login, registration, logout views + routes + user model.
* **Stripe Integration**

  * `z8 stripe_integr` → pricing page, checkout routes, webhook handler.
* **Database Layer**

  * Simple API (`db.insert()`, `db.query()`, `db.delete()`).
  * SQLite default, Postgres adapter option.
* **LLM Integration**

  * Built-in helpers: `ask()`, `summarize()`, `extract()`.
  * Easy model switching.
* **`z8 dev` Command**

  * Run development server with auto-reload.

---

## 📂 Project Structure

```
z8ter/              # Core framework code
    __init__.py     # Jinja templates init
    cli.py          # CLI entry point
    page.py         # Base Page class
views/              # Application page logic
templates/          # Jinja templates
components/         # Reusable UI components (e.g., base.jinja)
setup.py            # Package metadata & CLI config
```

---

## 🚀 Getting Started

### 1. Install Locally

```bash
pip install -e .
```

### 2. Create a New Page

```bash
z8 create_page about
```

### 3. Run the Dev Server

```bash
uvicorn app:app --reload
```

---

## 💡 Philosophy

Z8ter is designed to:

* Reduce boilerplate for common patterns (auth, Stripe, routing).
* Keep backend + frontend tightly coupled in development for speed.
* Make creating interactive pages as fast as possible.