"""
Data Seeding Module

Purpose:
- Load demo data from JSON files into SQLite database
- Support quick setup for development, testing, and demos
- Ensure reproducible data scenarios

Usage:
    # As module
    from app.data.seed_data import load_all_seeds
    conn = get_connection()
    init_db(conn)
    load_all_seeds(conn)
    
    # From command line
    python -m app.data.seed_data
"""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any


def get_seeds_dir() -> Path:
    """Get the seeds directory path."""
    return Path(__file__).parent / "seeds"


def load_json_file(filepath: Path) -> list[dict[str, Any]]:
    """
    Load JSON file and return data.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        List of records from JSON file
    """
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def load_departments(conn: sqlite3.Connection) -> None:
    """Load departments seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "departments.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            "INSERT OR REPLACE INTO departments (id, name) VALUES (?, ?)",
            (record["id"], record["name"])
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} departments")


def load_skills(conn: sqlite3.Connection) -> None:
    """Load skills seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "skills.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            "INSERT OR REPLACE INTO skills (id, name, category) VALUES (?, ?, ?)",
            (record["id"], record["name"], record["category"])
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} skills")


def load_employees(conn: sqlite3.Connection) -> None:
    """Load employees seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "employees.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO employees 
            (id, name, role, department_id, level, points_current, hire_date, 
             skills_map, courses_enrolled_map, goals_set)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"], 
                record["name"], 
                record["role"], 
                record["department_id"],
                record["level"], 
                record["points_current"], 
                record["hire_date"],
                record["skills_map"], 
                record["courses_enrolled_map"], 
                record["goals_set"]
            )
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} employees")


def load_courses(conn: sqlite3.Connection) -> None:
    """Load courses seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "courses.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO courses 
            (id, title, description, difficulty, duration_weeks, 
             effort_hours_week, points_reward, roi, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"], 
                record["title"], 
                record["description"],
                record["difficulty"], 
                record["duration_weeks"],
                record["effort_hours_week"], 
                record["points_reward"],
                record["roi"], 
                record["active"]
            )
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} courses")


def load_course_skills(conn: sqlite3.Connection) -> None:
    """Load course-skill mappings seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "course_skills.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO course_skills 
            (course_id, skill_id, weight)
            VALUES (?, ?, ?)
            """,
            (record["course_id"], record["skill_id"], record["weight"])
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} course-skill mappings")


def load_mentorship_profiles(conn: sqlite3.Connection) -> None:
    """Load mentorship profiles seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "mentorship_profiles.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO mentorship_profiles 
            (employee_id, is_mentor, capacity, mentees_count, rating, personality)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record["employee_id"], 
                record["is_mentor"],
                record["capacity"], 
                record["mentees_count"],
                record["rating"], 
                record["personality"]
            )
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} mentorship profiles")


def load_marketplace_items(conn: sqlite3.Connection) -> None:
    """Load marketplace items seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "marketplace_items.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO marketplace_items 
            (id, name, description, points_cost, category, in_stock)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"], 
                record["name"], 
                record["description"],
                record["points_cost"], 
                record["category"], 
                record["in_stock"]
            )
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} marketplace items")


def load_goals(conn: sqlite3.Connection) -> None:
    """Load goals seed data."""
    seeds_dir = get_seeds_dir()
    data = load_json_file(seeds_dir / "goals.json")
    
    cursor = conn.cursor()
    for record in data:
        cursor.execute(
            """
            INSERT INTO goals 
            (employee_id, title, target_date, progress_percent)
            VALUES (?, ?, ?, ?)
            """,
            (
                record["employee_id"], 
                record["title"],
                record["target_date"], 
                record["progress_percent"]
            )
        )
    conn.commit()
    print(f"✅ Loaded {len(data)} goals")


def load_all_seeds(conn: sqlite3.Connection) -> None:
    """
    Load all seed data in correct order (respecting foreign keys).
    
    Order matters:
    1. departments (no dependencies)
    2. employees (depends on departments)
    3. skills (no dependencies)
    4. courses (no dependencies)
    5. course_skills (depends on courses, skills)
    6. mentorship_profiles (depends on employees)
    7. marketplace_items (no dependencies)
    8. goals (depends on employees)
    
    Args:
        conn: SQLite database connection
    """
    print("\n🌱 Loading seed data...")
    print("=" * 50)
    
    try:
        # Load in correct order (FK dependencies)
        load_departments(conn)
        load_employees(conn)
        load_skills(conn)
        load_courses(conn)
        load_course_skills(conn)
        load_mentorship_profiles(conn)
        load_marketplace_items(conn)
        load_goals(conn)
        
        print("=" * 50)
        print("✅ All seed data loaded successfully!\n")
        
    except Exception as e:
        print(f"❌ Error loading seed data: {e}")
        conn.rollback()
        raise


if __name__ == "__main__":
    """
    Run this module directly to seed the database:
    
        python -m app.data.seed_data
    """
    from app.core.db import get_connection, init_db
    
    print("\n🚀 PSA Hackathon - Database Seeding")
    print("=" * 50)
    
    # Get connection and initialize database
    conn = get_connection()
    print("📁 Database location:", conn.execute("PRAGMA database_list").fetchone()[2])
    
    # Create tables if they don't exist
    print("\n🔧 Initializing database schema...")
    init_db(conn)
    print("✅ Database schema initialized")
    
    # Load all seed data
    load_all_seeds(conn)
    
    # Verify data loaded
    cursor = conn.cursor()
    stats = {
        "departments": cursor.execute("SELECT COUNT(*) FROM departments").fetchone()[0],
        "employees": cursor.execute("SELECT COUNT(*) FROM employees").fetchone()[0],
        "skills": cursor.execute("SELECT COUNT(*) FROM skills").fetchone()[0],
        "courses": cursor.execute("SELECT COUNT(*) FROM courses").fetchone()[0],
        "course_skills": cursor.execute("SELECT COUNT(*) FROM course_skills").fetchone()[0],
        "mentorship_profiles": cursor.execute("SELECT COUNT(*) FROM mentorship_profiles").fetchone()[0],
        "marketplace_items": cursor.execute("SELECT COUNT(*) FROM marketplace_items").fetchone()[0],
        "goals": cursor.execute("SELECT COUNT(*) FROM goals").fetchone()[0],
    }
    
    print("\n📊 Database Statistics:")
    print("=" * 50)
    for table, count in stats.items():
        print(f"  {table:.<30} {count:>3} records")
    
    print("=" * 50)
    print("✅ Seeding complete! Database ready for use.\n")
    
    conn.close()
