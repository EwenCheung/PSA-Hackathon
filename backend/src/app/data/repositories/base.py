"""
BaseRepository: Abstract base class for all repositories.
Provides common CRUD operations and connection management.
"""
from typing import Any, Generic, List, Optional, TypeVar
import sqlite3

T = TypeVar("T")

def dict_factory(cursor, row):
    """Convert sqlite3.Row to dict"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class BaseRepository(Generic[T]):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        # Set row_factory to return dicts
        self.conn.row_factory = sqlite3.Row

    def get_by_id(self, table: str, id_field: str, id_value: Any) -> Optional[dict]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE {id_field} = ?", (id_value,))
        row = cur.fetchone()
        return dict(row) if row else None

    def list_all(self, table: str) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def create(self, table: str, data: dict) -> int:
        cur = self.conn.cursor()
        keys = ','.join(data.keys())
        placeholders = ','.join(['?'] * len(data))
        cur.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", tuple(data.values()))
        self.conn.commit()
        return cur.lastrowid

    def update(self, table: str, id_field: str, id_value: Any, data: dict) -> int:
        cur = self.conn.cursor()
        set_clause = ','.join([f"{k}=?" for k in data.keys()])
        cur.execute(f"UPDATE {table} SET {set_clause} WHERE {id_field} = ?", tuple(data.values()) + (id_value,))
        self.conn.commit()
        return cur.rowcount

    def delete(self, table: str, id_field: str, id_value: Any) -> int:
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM {table} WHERE {id_field} = ?", (id_value,))
        self.conn.commit()
        return cur.rowcount
