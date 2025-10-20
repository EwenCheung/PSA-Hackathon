"""Utilities to keep mentor_match_requests schema up to date."""

from __future__ import annotations

import sqlite3


def ensure_mentor_request_history_schema(conn: sqlite3.Connection) -> None:
    """Ensure mentor_match_requests allows multiple historical entries per mentee."""

    cursor = conn.cursor()
    table_info = cursor.execute("PRAGMA table_info(mentor_match_requests)").fetchall()
    if not table_info:
        return

    indexes = cursor.execute("PRAGMA index_list(mentor_match_requests)").fetchall()
    has_unique_index = any(index[2] for index in indexes)  # index[2] is `unique`
    if not has_unique_index:
        return

    conn.execute("PRAGMA foreign_keys=OFF;")
    cursor.execute("BEGIN")
    cursor.execute("ALTER TABLE mentor_match_requests RENAME TO mentor_match_requests_old")

    cursor.execute(
        """
        CREATE TABLE mentor_match_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mentee_id TEXT NOT NULL,
            mentor_id TEXT NOT NULL,
            match_score REAL,
            explanation TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (mentee_id) REFERENCES employees(id),
            FOREIGN KEY (mentor_id) REFERENCES employees(id)
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO mentor_match_requests (
            id, mentee_id, mentor_id, match_score, explanation, status, created_at
        )
        SELECT id, mentee_id, mentor_id, match_score, explanation, status, created_at
        FROM mentor_match_requests_old
        """
    )

    cursor.execute("DROP TABLE mentor_match_requests_old")
    cursor.execute("COMMIT")
    conn.execute("PRAGMA foreign_keys=ON;")
