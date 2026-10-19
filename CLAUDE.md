# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Spendly is a personal expense tracker: log expenses, see where the money goes, and filter spending by date range. Amounts are in rupees (₹).

Built so far: the landing, register, login, terms, and privacy pages render. The register and login forms don't process input yet. Not built: database code, auth, profile, and expense CRUD.

## Architecture

- `app.py` is a single Flask app that holds every route. There are no blueprints yet.
- `templates/`: Jinja pages. Each one extends `base.html`, which provides the navbar and footer.
- `static/css/style.css` holds the shared styles. `static/css/landing.css` overrides them and is loaded only on the landing page.
- `static/js/main.js` is an empty placeholder. All JavaScript goes here.
- `database/` is the package for all SQLite code. `db.py` is still a stub.
- Known gap: the register and login forms POST to `/register` and `/login`, but those routes accept GET only. Add `methods=["GET", "POST"]` when the form handling step is built.

## Code style

- Python: double quotes, lines up to 88 characters, and the ruff rules E, F, and I (see `ruff.toml`).
- `app.py` groups routes under boxed `# ---- #` banner comments. Keep new routes in the matching group.
- Route functions are named after their page (`landing`, `login`) and return `render_template(...)`.
- Templates: 4-space indent. Page titles use the form `Page name — Spendly` with an em dash, e.g. `Sign in — Spendly`.
- CSS: each file has boxed section banners. Use the variables defined on `:root` in `style.css` (`--ink`, `--paper`, `--accent`, and so on) instead of hard-coded colors. Class names are lowercase and hyphenated, prefixed by component (`.auth-card`, `.hero-badge`).
- JavaScript is vanilla only, with no frameworks or libraries.

## Preferred libraries

- **Flask 3.1.3** for routing and rendering. Jinja2 comes with it, so use it for templates.
- **Python's built-in `sqlite3`** for the database. Use `row_factory` for dict-like rows, as the `get_db()` stub describes. Don't add an ORM.
- **pytest 8.3.5 with pytest-flask 1.3.0** for tests.
- **ruff** for linting (installed in the venv, not pinned in `requirements.txt`).
- **DM Serif Display and DM Sans** from Google Fonts, already linked in `base.html`.

## Critical rules

- Build only the step the user asks for. Don't implement placeholder routes or the `database/db.py` stubs ahead of time.
- All SQL goes in `database/db.py`. `app.py` never contains SQL.
- Don't add a dependency to `requirements.txt` without asking. Keep every pin as an exact version (`==`).
- `debug=True` in `app.py` is for local runs only. Don't ship it as-is.
- Never commit `venv/`, `expense_tracker.db`, or `.env`.
- Routes that handle form submissions must declare `methods=["GET", "POST"]`.

## Commands

- Setup: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Run: `python app.py` (serves on http://localhost:5001 in debug mode)
- Test: `pytest` (pytest-flask is installed, but no tests exist yet)
- Lint: `venv/bin/ruff check .` (config in `ruff.toml`; ruff is installed in the venv but not listed in `requirements.txt`)

## Project status

This is a step-by-step course project. Routes that return "coming in Step N" in `app.py`, and the stubs in `database/db.py`, are placeholders for later steps.

## Development roadmap

Steps are taken from the placeholder comments in the code. Build them in order. Steps 2, 5, and 6 aren't named in the code yet.

1. Database setup: `get_db()`, `init_db()`, `seed_db()` in `database/db.py`. Not built.
2. Not specified in the code yet.
3. Logout (`/logout` placeholder in `app.py`). Not built.
4. Profile page (`/profile` placeholder). Not built.
5. Not specified in the code yet.
6. Not specified in the code yet.
7. Add expense (`/expenses/add` placeholder). Not built.
8. Edit expense (`/expenses/<int:id>/edit` placeholder). Not built.
9. Delete expense (`/expenses/<int:id>/delete` placeholder). Not built.

## Conventions

- Templates extend `templates/base.html`. Page-specific stylesheets are linked in that template's `{% block head %}`, e.g. `landing.css` in `landing.html`, not in `base.html`.
- Commit messages use `<area>: <lowercase description>`, e.g. `landing: add privacy policy page and route`.
