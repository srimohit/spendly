# Spec: Login and Logout

## Overview
Login was already specced and implemented separately (`.claude/specs/05-login.md`) and is now merged into `main` — it is not re-specified here, only depended on. The remaining piece of the auth pair is **Logout**, which is roadmap Step 3's named placeholder in `app.py`. This step clears the Flask `session` that Login starts and sends the user back to `/login`, and updates the shared navbar so it reflects whether someone is signed in (showing "Sign out" instead of "Sign in" / "Get started").

## Depends on
- Step 1 (Database setup) — `users` table, `get_db()`.
- Step 5 (Login) — already complete and merged to `main`. Login sets `session["user_id"]` and `session["user_name"]`; Logout is the piece that clears them.

## Routes
- `GET /logout` — clears the session and redirects to `/login` — logged-in (also safe to call with no active session; it's a no-op redirect rather than an error)

## Database changes
No database changes. Logout only touches the Flask `session` cookie, not the `users` table.

## Templates
- **Create:** none
- **Modify:** `templates/base.html` — in the `.nav-links` block, show a "Sign out" link (`href="{{ url_for('logout') }}"`, reusing the existing `.nav-cta` class) when `session.user_id` is set; otherwise keep the current "Sign in" / "Get started" links. `session` is available in Jinja automatically via Flask, so no route changes are needed on other pages for this to work.
  - **Boundary note:** `base.html` is listed in CLAUDE.md as "ask before changing" since every page inherits from it — confirm before editing it during implementation.

## Files to change
- `app.py` — implement the `/logout` route: `session.clear()` then `redirect(url_for("login"))`. Move it out of the "Placeholder routes" boxed section into the main "Routes" section, since it's no longer a stub.
- `templates/base.html` — conditional navbar links described above (ask first, per the boundary note).

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Don't re-implement any part of Login — it's already merged; only add Logout
- Use `session.clear()` rather than popping individual keys, so no stray session state survives a logout
- `/logout` must not error when there is no active session — it should just redirect to `/login` either way
- Ask before editing `templates/base.html`, per CLAUDE.md's boundary rules

## Definition of done
- [ ] `GET /logout` clears the session (cookie no longer carries `user_id`/`user_name`) and redirects to `/login`
- [ ] Visiting `/logout` while already logged out does not error — it still redirects to `/login`
- [ ] After logging in, the navbar shows a "Sign out" link instead of "Sign in" / "Get started"
- [ ] Clicking "Sign out" returns the navbar to the logged-out state ("Sign in" / "Get started")
- [ ] Existing Login behavior (`GET`/`POST /login`) is unchanged
- [ ] `venv/bin/ruff check .` passes with no new errors
