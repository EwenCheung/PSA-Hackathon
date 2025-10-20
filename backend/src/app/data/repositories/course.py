"""
CourseRepository: Data access and management for courses table.
Automatically syncs with courses.json at startup.
"""
from typing import Optional, List, Dict, Any
import sqlite3
import json
from pathlib import Path
from .base import BaseRepository

JSON_FILE = Path(__file__).parent.parent / "seeds" / "courses.json"

class CourseRepository(BaseRepository):
    TABLE = "courses"
    ID_FIELD = "id"

    def __init__(self, conn: sqlite3.Connection, auto_sync: bool = True):
        super().__init__(conn)
        self.conn.row_factory = sqlite3.Row  # For dict conversion
        if auto_sync:
            self.sync_from_json()

    def sync_from_json(self):
        """Load courses.json and sync the database table."""
        if not JSON_FILE.exists():
            print(f"Warning: {JSON_FILE} does not exist.")
            return

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            courses = json.load(f)

        cur = self.conn.cursor()
        
        # Drop existing table completely
        cur.execute(f"DROP TABLE IF EXISTS {self.TABLE}")
        
        # Create fresh table with correct schema matching JSON
        cur.execute(f"""
            CREATE TABLE {self.TABLE} (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                difficulty TEXT,
                duration_weeks INTEGER,
                effort_hours_week INTEGER,
                points_reward INTEGER,
                roi TEXT,
                url TEXT,
                active INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

        # Insert all data from JSON
        query = f"""
            INSERT INTO {self.TABLE}
            (id, title, description, difficulty, duration_weeks, effort_hours_week,
             points_reward, roi, url, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = [
            (c["id"], c["title"], c["description"], c["difficulty"],
             c["duration_weeks"], c["effort_hours_week"], c["points_reward"],
             c["roi"], c["url"], c.get("active", 1))
            for c in courses
        ]
        cur.executemany(query, data)
        self.conn.commit()
        print(f"Synced {len(data)} courses from JSON into {self.TABLE}.")

    def get_course(self, course_id: str) -> Optional[dict]:
        """Retrieve a single course by ID."""
        cur = self.conn.cursor()
        query = f"SELECT * FROM {self.TABLE} WHERE {self.ID_FIELD} = ?"
        cur.execute(query, (course_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def list_courses(self) -> List[dict]:
        """List all active courses."""
        cur = self.conn.cursor()
        query = f"SELECT * FROM {self.TABLE} WHERE active = 1"
        cur.execute(query)
        return [dict(row) for row in cur.fetchall()]

    def search_courses(self, keyword: str) -> List[dict]:
        """Search courses by keyword in title or description."""
        cur = self.conn.cursor()
        query = f"""
            SELECT * FROM {self.TABLE}
            WHERE (title LIKE ? OR description LIKE ?)
            AND active = 1
        """
        like_term = f"%{keyword}%"
        cur.execute(query, (like_term, like_term))
        return [dict(row) for row in cur.fetchall()]

    def filter_by_difficulty(self, difficulty: str) -> List[dict]:
        """List courses filtered by difficulty level."""
        cur = self.conn.cursor()
        query = f"SELECT * FROM {self.TABLE} WHERE difficulty = ? AND active = 1"
        cur.execute(query, (difficulty,))
        return [dict(row) for row in cur.fetchall()]

    def list_top_courses(self, limit: int = 5) -> List[dict]:
        """List top courses based on points_reward (e.g., for leaderboard or recommendations)."""
        cur = self.conn.cursor()
        query = f"""
            SELECT * FROM {self.TABLE}
            WHERE active = 1
            ORDER BY points_reward DESC
            LIMIT ?
        """
        cur.execute(query, (limit,))
        return [dict(row) for row in cur.fetchall()]

    def add_course(self, course: Dict[str, Any]) -> None:
        """Insert a new course record."""
        cur = self.conn.cursor()
        query = f"""
            INSERT INTO {self.TABLE}
            (id, title, description, difficulty, duration_weeks, effort_hours_week,
             points_reward, roi, url, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(query, (
            course["id"], course["title"], course["description"], course["difficulty"],
            course["duration_weeks"], course["effort_hours_week"], course["points_reward"],
            course["roi"], course["url"], course["active"]
        ))
        self.conn.commit()

    def bulk_insert(self, courses: List[Dict[str, Any]]) -> None:
        """Batch insert multiple courses (used for seeding from JSON)."""
        cur = self.conn.cursor()
        query = f"""
            INSERT INTO {self.TABLE}
            (id, title, description, difficulty, duration_weeks, effort_hours_week,
             points_reward, roi, url, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = [
            (c["id"], c["title"], c["description"], c["difficulty"],
             c["duration_weeks"], c["effort_hours_week"], c["points_reward"],
             c["roi"], c["url"], c.get("active", 1))
            for c in courses
        ]
        cur.executemany(query, data)
        self.conn.commit()

    def deactivate_course(self, course_id: str) -> None:
        """Deactivate a course (soft delete)."""
        cur = self.conn.cursor()
        query = f"UPDATE {self.TABLE} SET active = 0 WHERE {self.ID_FIELD} = ?"
        cur.execute(query, (course_id,))
        self.conn.commit()

    def delete_course(self, course_id: str) -> None:
        """Permanently delete a course (use with caution)."""
        cur = self.conn.cursor()
        query = f"DELETE FROM {self.TABLE} WHERE {self.ID_FIELD} = ?"
        cur.execute(query, (course_id,))
        self.conn.commit()