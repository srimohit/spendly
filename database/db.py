import os
import sqlite3

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "expense_tracker.db",
)

SAMPLE_EXPENSES = [
    (1450.00, "Bills", "2026-10-01", "BESCOM electricity bill"),
    (320.00, "Food", "2026-10-03", "Swiggy lunch order"),
    (180.00, "Transport", "2026-10-05", "Ola ride to office"),
    (650.00, "Health", "2026-10-07", "Apollo Pharmacy medicines"),
    (499.00, "Entertainment", "2026-10-10", "Netflix monthly subscription"),
    (2499.00, "Shopping", "2026-10-13", "Myntra sneakers"),
    (250.00, "Other", "2026-10-16", "Birthday gift for a colleague"),
    (640.00, "Food", "2026-10-18", "Zomato dinner with friends"),
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                amount REAL NOT NULL CHECK (amount > 0),
                category TEXT NOT NULL
                    CHECK (category IN (
                        'Food', 'Transport', 'Bills', 'Health',
                        'Entertainment', 'Shopping', 'Other'
                    )),
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count > 0:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        for amount, category, date, description in SAMPLE_EXPENSES:
            conn.execute(
                """
                INSERT INTO expenses (user_id, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, amount, category, date, description),
            )
        conn.commit()
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()
