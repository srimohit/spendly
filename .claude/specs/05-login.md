# Spec: Login

## Overview
This step wires up the `/login` form so a registered user can actually sign in. The `login.html` template already renders and posts to `/login`, but the route only accepts `GET`. This step adds `POST` handling: look up the user by email, verify the password against its hash, and start a logged-in session using Flask's built-in `session`. This is the step that introduces session state for the app — later steps (Logout, Profile) will read `session["user_id"]` to know who is signed in.

## Depends on
- Step 1 (Database setup) — requires the `users` table and `get_db()` from `database/db.py`.
- Step 02 (Registration) — a user must exist (with a hashed password) to log in. If `get_user_by_email()` wasn't already added to `database/db.py` by that step on this branch, add it here instead of duplicating it later.

## Routes
- `GET /login` — render the empty login form — public (already implemented)
- `POST /login` — validate credentials, start the session on success, or re-render the form with an error on failure — public

## Database changes
No database changes. Uses the existing `users` table from Step 1 (`email`, `password_hash`). Only a query function is added to `database/db.py`, not a schema change.

## Templates
- **Create:** none
- **Modify:** `templates/login.html` — repopulate the `email` input with the previously submitted value (`value="{{ email or '' }}"`) so the form stays filled in when an error is shown. No structural changes to the form itself.

## Files to change
- `app.py`:
  - Set `app.secret_key` from `os.environ.get("SECRET_KEY", "dev-secret-key")` so Flask's `session` can sign its cookie
  - Change `@app.route("/login")` to `methods=["GET", "POST"]`
  - On `POST`: validate input, call `get_user_by_email()`, verify the password with `check_password_hash()`, and on success set `session["user_id"]` and `session["user_name"]`, then redirect to `/profile`; on failure re-render `login.html` with `error` and the submitted `email`
- `database/db.py` — add `get_user_by_email(email)` (parameterized `SELECT` by email) if it does not already exist on this branch
- `templates/login.html` — add `value="{{ email or '' }}"` to the email input

## Files to create
None.

## New dependencies
No new dependencies. Flask's `session` is built-in; no extra package is needed for the secret key (read via `os.environ`, standard library).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with werkzeug's `check_password_hash` (never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- All SQL stays in `database/db.py`; `app.py` only calls those functions
- Use one generic error message ("Invalid email or password.") for both "no such email" and "wrong password" — don't reveal which one was wrong
- Validate server-side that email and password are both non-empty before querying the database
- On success, store only `user_id` and `user_name` in the session — never the password or password hash
- Redirect (302) to `/profile` on success; `/profile` still returns its Step 4 placeholder text, which is expected at this stage

## Definition of done
- [ ] Visiting `/login` still renders the empty form (GET unchanged)
- [ ] Submitting the demo user's correct email/password redirects to `/profile` and sets a session cookie
- [ ] Submitting a correct email with the wrong password re-renders `login.html` with "Invalid email or password." and does not start a session
- [ ] Submitting an email that doesn't exist re-renders `login.html` with the same "Invalid email or password." message
- [ ] Submitting an empty email or empty password re-renders the form with an error and does not query the database
- [ ] On a re-rendered error, the previously typed email is still filled in
- [ ] `venv/bin/ruff check .` passes with no new errors
