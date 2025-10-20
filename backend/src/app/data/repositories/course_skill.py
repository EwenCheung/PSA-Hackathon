"""
CourseSkillRepository: Data access and management for course_skills table.
Automatically syncs with course_skills.json at startup.
"""
from typing import List, Dict, Any
import sqlite3
import json
from pathlib import Path
from .base import BaseRepository

JSON_FILE = Path(__file__).parent.parent / "seeds" / "course_skills.json"

class CourseSkillRepository(BaseRepository):
    TABLE = "course_skills"

    def __init__(self, conn: sqlite3.Connection, auto_sync: bool = True):
        super().__init__(conn)
        self.conn.row_factory = sqlite3.Row  # For dict conversion
        if auto_sync:
            self.sync_from_json()

    def sync_from_json(self):
        """Load course_skills.json and sync the database table."""
        if not JSON_FILE.exists():
            print(f"Warning: {JSON_FILE} does not exist.")
            return

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            course_skills = json.load(f)

        # Create table if not exists
        cur = self.conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE} (
                course_id TEXT,
                skill_id TEXT,
                weight INTEGER
            )
        """)
        self.conn.commit()

        # Clear old data and insert JSON data
        cur.execute(f"DELETE FROM {self.TABLE}")
        self.conn.commit()

        query = f"INSERT INTO {self.TABLE} (course_id, skill_id, weight) VALUES (?, ?, ?)"
        data = [(cs["course_id"], cs["skill_id"], cs["weight"]) for cs in course_skills]
        cur.executemany(query, data)
        self.conn.commit()
        print(f"Synced {len(data)} course-skills from JSON into {self.TABLE}.")

    def list_course_skills(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.TABLE}")
        return [dict(row) for row in cur.fetchall()]

    def get_skills_for_course(self, course_id: str) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        query = f"""
            SELECT cs.skill_id, cs.weight
            FROM {self.TABLE} cs
            WHERE cs.course_id = ?
        """
        cur.execute(query, (course_id,))
        return [dict(row) for row in cur.fetchall()]

    def get_courses_for_skill(self, skill_id: str) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        query = f"""
            SELECT cs.course_id, cs.weight
            FROM {self.TABLE} cs
            WHERE cs.skill_id = ?
        """
        cur.execute(query, (skill_id,))
        return [dict(row) for row in cur.fetchall()]

    def add_course_skill(self, course_skill: Dict[str, Any]) -> None:
        cur = self.conn.cursor()
        query = f"INSERT INTO {self.TABLE} (course_id, skill_id, weight) VALUES (?, ?, ?)"
        cur.execute(query, (course_skill["course_id"], course_skill["skill_id"], course_skill["weight"]))
        self.conn.commit()

    def bulk_insert(self, course_skills: List[Dict[str, Any]]) -> None:
        cur = self.conn.cursor()
        query = f"INSERT INTO {self.TABLE} (course_id, skill_id, weight) VALUES (?, ?, ?)"
        data = [(cs["course_id"], cs["skill_id"], cs["weight"]) for cs in course_skills]
        cur.executemany(query, data)
        self.conn.commit()
