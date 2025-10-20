"""
Core: db (SQLite helper)

Purpose
- Provide helpers to create a SQLite connection and initialize minimal schema.

Notes
- Uses Python stdlib `sqlite3` to avoid external dependencies.
"""
from __future__ import annotations

import os
import sqlite3
from typing import Iterable, Mapping

from app.data.migrations import (
    ensure_position_level_column,
    ensure_mentor_request_history_schema,
)
from app.data.utils.position_level import derive_position_level


def get_connection(url: str | None = None) -> sqlite3.Connection:
    """
    Get SQLite database connection.
    
    Args:
        url: Database URL. Defaults to data/database/app.db or DATABASE_URL env var.
    
    Returns:
        SQLite connection with foreign keys enabled.
    
    Note:
        - Default path: backend/src/app/data/database/app.db
        - Use ':memory:' for in-memory database (testing)
        - Creates parent directories automatically
    """
    # Default to data/database/app.db (not root level)
    default_path = os.path.join(os.path.dirname(__file__), "..", "data", "database", "app.db")
    db_url = url or os.getenv("DATABASE_URL", default_path)
    
    # Handle in-memory database for testing
    if db_url == ":memory:":
        conn = sqlite3.connect(db_url, check_same_thread=False)
    else:
        # Create data/database/ directory if it doesn't exist
        db_path = os.path.abspath(db_url)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Ensure foreign key constraints are enforced
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # Core
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS departments (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            department_id TEXT,
            level TEXT,
            position_level INTEGER,
            points_current INTEGER DEFAULT 0,
            hire_date TEXT,
            skills_map TEXT,
            courses_enrolled_map TEXT,
            goals_set TEXT,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT
        )
        """
    )

    # Learning & Goals
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            difficulty TEXT,
            duration_weeks INTEGER,
            effort_hours_week INTEGER,
            points_reward INTEGER,
            roi TEXT,
            active INTEGER DEFAULT 1
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS course_skills (
            course_id TEXT,
            skill_id TEXT,
            weight INTEGER,
            PRIMARY KEY (course_id, skill_id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (skill_id) REFERENCES skills(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS enrollments (
            employee_id TEXT,
            course_id TEXT,
            status TEXT,
            progress_percent INTEGER,
            started_at TEXT,
            completed_at TEXT,
            points_awarded INTEGER,
            PRIMARY KEY (employee_id, course_id),
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            title TEXT,
            target_date TEXT,
            progress_percent INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """
    )

    # Wellbeing
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS wellbeing_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            anon_session_id TEXT,
            sender TEXT,
            content TEXT,
            timestamp TEXT,
            is_anonymous INTEGER DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiment_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            label TEXT,
            score REAL,
            confidence REAL,
            created_at TEXT,
            FOREIGN KEY (message_id) REFERENCES wellbeing_messages(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiment_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            anon_session_id TEXT,
            day TEXT,
            label TEXT,
            average_score REAL,
            messages_count INTEGER,
            created_at TEXT
        )
        """
    )

    # Mentorship
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mentorship_profiles (
            employee_id TEXT PRIMARY KEY,
            is_mentor INTEGER DEFAULT 0,
            capacity INTEGER,
            mentees_count INTEGER,
            rating REAL,
            personality TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mentorship_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mentor_id TEXT,
            mentee_id TEXT,
            score REAL,
            reasons_json TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (mentor_id) REFERENCES employees(id),
            FOREIGN KEY (mentee_id) REFERENCES employees(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mentor_match_requests (
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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mentor_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mentor_id TEXT,
            mentee_id TEXT,
            session_date TEXT,
            notes TEXT,
            points_awarded INTEGER,
            FOREIGN KEY (mentor_id) REFERENCES employees(id),
            FOREIGN KEY (mentee_id) REFERENCES employees(id)
        )
        """
    )

    ensure_mentor_request_history_schema(conn)

    # Rewards & Points
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketplace_items (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            points_cost INTEGER,
            category TEXT,
            in_stock INTEGER DEFAULT 1
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS redemptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            item_id INTEGER,
            points_cost INTEGER,
            created_at TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (item_id) REFERENCES marketplace_items(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS points_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            delta INTEGER,
            source TEXT,
            reference_id TEXT,
            created_at TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """
    )

    # Advanced
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leadership_potential_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            model_version TEXT,
            score REAL,
            label TEXT,
            factors_json TEXT,
            created_at TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """
    )

    # Indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_enrollments_emp ON enrollments(employee_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_enrollments_course ON enrollments(course_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wellbeing_emp_time ON wellbeing_messages(employee_id, timestamp);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sentiment_msg ON sentiment_messages(message_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_emp_day ON sentiment_snapshots(employee_id, day);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_matches_mentor ON mentorship_matches(mentor_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_matches_mentee ON mentorship_matches(mentee_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_requests_mentee ON mentor_match_requests(mentee_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_points_emp_time ON points_ledger(employee_id, created_at);")

    conn.commit()
    ensure_position_level_column(conn)


def seed_employees(conn: sqlite3.Connection, rows: Iterable[Mapping]) -> None:
    cur = conn.cursor()
    prepared = []
    for row in rows:
        row_dict = dict(row)
        prepared.append(
            {
                "id": row_dict.get("id"),
                "name": row_dict.get("name"),
                "role": row_dict.get("role"),
                "department_id": row_dict.get("department_id"),
                "level": row_dict.get("level"),
                "position_level": derive_position_level(
                    row_dict.get("level"), row_dict.get("position_level")
                ),
                "points_current": row_dict.get("points_current", 0),
                "hire_date": row_dict.get("hire_date"),
                "skills_map": row_dict.get("skills_map"),
                "courses_enrolled_map": row_dict.get("courses_enrolled_map"),
                "goals_set": row_dict.get("goals_set"),
            }
        )
    cur.executemany(
        """
        INSERT OR REPLACE INTO employees (
            id, name, role, department_id, level, position_level, points_current,
            hire_date, skills_map, courses_enrolled_map, goals_set
        )
        VALUES (
            :id, :name, :role, :department_id, :level, :position_level, :points_current,
            :hire_date, :skills_map, :courses_enrolled_map, :goals_set
        )
        """,
        prepared,
    )
    conn.commit()
