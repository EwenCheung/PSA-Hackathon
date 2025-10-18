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
        return self.get_by_id(self.TABLE, self.ID_FIELD, course_id)

    def list_courses(self) -> List[dict]:
        """List all active courses."""
        query = f"SELECT * FROM {self.TABLE} WHERE active = 1"
        return self.fetchall(query)

    def search_courses(self, keyword: str) -> List[dict]:
        """Search courses by keyword in title or description."""
        query = f"""
            SELECT * FROM {self.TABLE}
            WHERE (title LIKE ? OR description LIKE ?)
            AND active = 1
        """
        like_term = f"%{keyword}%"
        return self.fetchall(query, (like_term, like_term))

    def filter_by_difficulty(self, difficulty: str) -> List[dict]:
        """List courses filtered by difficulty level."""
        query = f"SELECT * FROM {self.TABLE} WHERE difficulty = ? AND active = 1"
        return self.fetchall(query, (difficulty,))

    def list_top_courses(self, limit: int = 5) -> List[dict]:
        """List top courses based on points_reward (e.g., for leaderboard or recommendations)."""
        query = f"""
            SELECT * FROM {self.TABLE}
            WHERE active = 1
            ORDER BY points_reward DESC
            LIMIT ?
        """
        return self.fetchall(query, (limit,))

    def add_course(self, course: Dict[str, Any]) -> None:
        """Insert a new course record."""
        query = f"""
            INSERT INTO {self.TABLE}
            (id, title, description, difficulty, duration_weeks, effort_hours_week,
             points_reward, roi, url, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(query, (
            course["id"], course["title"], course["description"], course["difficulty"],
            course["duration_weeks"], course["effort_hours_week"], course["points_reward"],
            course["roi"], course["url"], course["active"]
        ))

    def bulk_insert(self, courses: List[Dict[str, Any]]) -> None:
        """Batch insert multiple courses (used for seeding from JSON)."""
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
        self.executemany(query, data)

    def deactivate_course(self, course_id: str) -> None:
        """Deactivate a course (soft delete)."""
        query = f"UPDATE {self.TABLE} SET active = 0 WHERE {self.ID_FIELD} = ?"
        self.execute(query, (course_id,))

    def delete_course(self, course_id: str) -> None:
        """Permanently delete a course (use with caution)."""
        query = f"DELETE FROM {self.TABLE} WHERE {self.ID_FIELD} = ?"
        self.execute(query, (course_id,))