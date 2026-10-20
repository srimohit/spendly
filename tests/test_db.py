import sqlite3

import pytest

from database import db


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))


def count_expenses():
    conn = db.get_db()
    try:
        return conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    finally:
        conn.close()


def count_users():
    conn = db.get_db()
    try:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    finally:
        conn.close()


def test_get_db_returns_named_rows_with_foreign_keys_on(temp_db):
    conn = db.get_db()
    try:
        assert isinstance(conn, sqlite3.Connection)
        row = conn.execute("SELECT 42 AS amount").fetchone()
        assert row["amount"] == 42
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    finally:
        conn.close()


def test_init_db_creates_expenses_table(temp_db):
    db.init_db()
    assert count_expenses() == 0


def test_init_db_twice_keeps_existing_rows(temp_db):
    db.init_db()
    db.seed_db()
    db.init_db()
    assert count_expenses() == len(db.SAMPLE_EXPENSES)


def test_seed_db_adds_sample_expenses(temp_db):
    db.init_db()
    db.seed_db()
    assert count_expenses() == len(db.SAMPLE_EXPENSES)


def test_seed_db_twice_adds_no_duplicates(temp_db):
    db.init_db()
    db.seed_db()
    db.seed_db()
    assert count_expenses() == len(db.SAMPLE_EXPENSES)


def test_seed_db_before_init_db_raises(temp_db):
    with pytest.raises(sqlite3.OperationalError, match="no such table"):
        db.seed_db()


def test_database_refuses_zero_amount(temp_db):
    db.init_db()
    conn = db.get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Test User", "test@example.com", "hash"),
        )
        user_id = cursor.lastrowid
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO expenses (user_id, amount, category, date) "
                "VALUES (?, 0, 'Food', '2026-10-01')",
                (user_id,),
            )
    finally:
        conn.close()


def test_init_db_creates_users_table(temp_db):
    db.init_db()
    assert count_users() == 0


def test_seed_db_creates_demo_user_with_hashed_password(temp_db):
    db.init_db()
    db.seed_db()
    conn = db.get_db()
    try:
        row = conn.execute(
            "SELECT name, email, password_hash FROM users WHERE email = ?",
            ("demo@spendly.com",),
        ).fetchone()
    finally:
        conn.close()
    assert row is not None
    assert row["name"] == "Demo User"
    assert row["password_hash"] != "demo123"
    assert row["password_hash"].startswith(("pbkdf2:", "scrypt:"))


def test_seed_db_twice_adds_no_duplicate_users(temp_db):
    db.init_db()
    db.seed_db()
    db.seed_db()
    assert count_users() == 1


def test_seed_db_covers_all_categories(temp_db):
    db.init_db()
    db.seed_db()
    conn = db.get_db()
    try:
        rows = conn.execute("SELECT DISTINCT category FROM expenses").fetchall()
    finally:
        conn.close()
    categories = {row["category"] for row in rows}
    expected = {
        "Food",
        "Transport",
        "Bills",
        "Health",
        "Entertainment",
        "Shopping",
        "Other",
    }
    assert expected <= categories


def test_duplicate_email_insert_fails(temp_db):
    db.init_db()
    conn = db.get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("A", "dup@example.com", "hash1"),
        )
        conn.commit()
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("B", "dup@example.com", "hash2"),
            )
    finally:
        conn.close()


def test_expense_with_invalid_user_id_fails_fk(temp_db):
    db.init_db()
    conn = db.get_db()
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO expenses (user_id, amount, category, date) "
                "VALUES (9999, 100, 'Food', '2026-10-01')"
            )
    finally:
        conn.close()
