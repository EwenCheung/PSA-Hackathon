"""Ensure employees table has a numeric position_level column."""
from __future__ import annotations

import sqlite3
from typing import Iterable

from app.data.utils.position_level import derive_position_level


def _has_position_level_column(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(employees);")
    columns = {row[1] for row in cursor.fetchall()}
    return "position_level" in columns


def _backfill_position_levels(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT id, level, position_level FROM employees;")
    rows = cursor.fetchall()
    updates: list[tuple[int, str]] = []
    for row in rows:
        employee_id = row[0]
        level_text = row[1]
        explicit = row[2]
        derived = derive_position_level(level_text, explicit)
        updates.append((derived, employee_id))

    cursor.executemany(
        "UPDATE employees SET position_level = ? WHERE id = ?",
        updates,
    )
    conn.commit()


def ensure_position_level_column(conn: sqlite3.Connection) -> None:
    """
    Add the position_level column to employees if necessary and backfill values.
    """

    if not _has_position_level_column(conn):
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE employees ADD COLUMN position_level INTEGER;")
        conn.commit()

    _backfill_position_levels(conn)
