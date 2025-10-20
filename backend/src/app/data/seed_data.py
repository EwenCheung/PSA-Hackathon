# """
# Data Seeding Module

# Purpose:
# - Load demo data from JSON files into SQLite database
# - Support quick setup for development, testing, and demos
# - Ensure reproducible data scenarios

# Usage:
#     # As module
#     from app.data.seed_data import load_all_seeds
#     conn = get_connection()
#     init_db(conn)
#     load_all_seeds(conn)
    
#     # From command line
#     python -m app.data.seed_data
# """
# from __future__ import annotations

# import json
# import os
# import sqlite3
# from pathlib import Path
# from typing import Any

# from app.data.utils.position_level import derive_position_level


# def get_seeds_dir() -> Path:
#     """Get the seeds directory path."""
#     return Path(__file__).parent / "seeds"


# def load_json_file(filepath: Path) -> list[dict[str, Any]]:
#     """
#     Load JSON file and return data.
    
#     Args:
#         filepath: Path to JSON file
    
#     Returns:
#         List of records from JSON file
#     """
#     with open(filepath, encoding="utf-8") as f:
#         return json.load(f)


# def load_departments(conn: sqlite3.Connection) -> None:
#     """Load departments seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "departments.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             "INSERT OR REPLACE INTO departments (id, name) VALUES (?, ?)",
#             (record["id"], record["name"])
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} departments")


# def load_skills(conn: sqlite3.Connection) -> None:
#     """Load skills seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "skills.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             "INSERT OR REPLACE INTO skills (id, name, category) VALUES (?, ?, ?)",
#             (record["id"], record["name"], record["category"])
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} skills")


# def load_employees(conn: sqlite3.Connection) -> None:
#     """Load employees seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "employees.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         position_level = derive_position_level(record.get("level"), record.get("position_level"))
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO employees 
#             (id, name, role, department_id, level, position_level, points_current, hire_date, 
#              skills_map, courses_enrolled_map, goals_set)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["id"], 
#                 record["name"], 
#                 record["role"], 
#                 record["department_id"],
#                 record["level"], 
#                 position_level,
#                 record["points_current"], 
#                 record["hire_date"],
#                 record["skills_map"], 
#                 record["courses_enrolled_map"], 
#                 record["goals_set"]
#             )
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} employees")


# def load_courses(conn: sqlite3.Connection) -> None:
#     """Load courses seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "courses.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO courses 
#             (id, title, description, difficulty, duration_weeks, 
#              effort_hours_week, points_reward, roi, active)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["id"], 
#                 record["title"], 
#                 record["description"],
#                 record["difficulty"], 
#                 record["duration_weeks"],
#                 record["effort_hours_week"], 
#                 record["points_reward"],
#                 record["roi"], 
#                 record["active"]
#             )
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} courses")


# def load_course_skills(conn: sqlite3.Connection) -> None:
#     """Load course-skill mappings seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "course_skills.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO course_skills 
#             (course_id, skill_id, weight)
#             VALUES (?, ?, ?)
#             """,
#             (record["course_id"], record["skill_id"], record["weight"])
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} course-skill mappings")


# def load_mentorship_profiles(conn: sqlite3.Connection) -> None:
#     """Load mentorship profiles seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "mentorship_profiles.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO mentorship_profiles 
#             (employee_id, is_mentor, capacity, mentees_count, rating, personality)
#             VALUES (?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["employee_id"], 
#                 record["is_mentor"],
#                 record["capacity"], 
#                 record["mentees_count"],
#                 record["rating"], 
#                 record["personality"]
#             )
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} mentorship profiles")


# def load_marketplace_items(conn: sqlite3.Connection) -> None:
#     """Load marketplace items seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "marketplace_items.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO marketplace_items 
#             (id, name, description, points_cost, category, in_stock)
#             VALUES (?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["id"], 
#                 record["name"], 
#                 record["description"],
#                 record["points_cost"], 
#                 record["category"], 
#                 record["in_stock"]
#             )
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} marketplace items")


# def load_goals(conn: sqlite3.Connection) -> None:
#     """Load goals seed data."""
#     seeds_dir = get_seeds_dir()
#     data = load_json_file(seeds_dir / "goals.json")
    
#     cursor = conn.cursor()
#     for record in data:
#         cursor.execute(
#             """
#             INSERT INTO goals 
#             (employee_id, title, target_date, progress_percent)
#             VALUES (?, ?, ?, ?)
#             """,
#             (
#                 record["employee_id"], 
#                 record["title"],
#                 record["target_date"], 
#                 record["progress_percent"]
#             )
#         )
#     conn.commit()
#     print(f"✅ Loaded {len(data)} goals")


# def load_wellbeing_seeds(conn: sqlite3.Connection) -> None:
#     """Load wellbeing seed data."""
#     seeds_dir = get_seeds_dir()
#     data_messages = load_json_file(seeds_dir / "wellbeing_messages.json")
#     data_snapshots = load_json_file(seeds_dir / "sentiment_snapshot.json")
#     data_sentiments = load_json_file(seeds_dir / "sentiment_messages.json")
    
#     cursor = conn.cursor()
    
#     # Load wellbeing messages
#     for record in data_messages:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO wellbeing_messages 
#             (id, employee_id, anon_session_id, sender, content, timestamp, is_anonymous)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["id"], record["employee_id"], record.get("anon_session_id"),
#                 record["sender"], record["content"], record["timestamp"], record["is_anonymous"]
#             )
#         )
        
#     # Load sentiment snapshots
#     for record in data_snapshots:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO sentiment_snapshots
#             (id, employee_id, anon_session_id, day, label, average_score, messages_count, created_at)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["id"], record["employee_id"], record.get("anon_session_id"),
#                 record["day"], record["label"], record["average_score"], 
#                 record["messages_count"], record["created_at"]
#             )
#         )
    
#     # Load sentiment messages
#     for record in data_sentiments:
#         cursor.execute(
#             """
#             INSERT OR REPLACE INTO sentiment_messages
#             (id, message_id, label, score, confidence, created_at)
#             VALUES (?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 record["id"], record["message_id"], record["label"],
#                 record["score"], record["confidence"], record["created_at"]
#             )
#         )
    
#     conn.commit()
#     print(f"✅ Loaded wellbeing seed data")


# def load_all_seeds(conn: sqlite3.Connection) -> None:
#     """
#     Load all seed data in correct order (respecting foreign keys).
    
#     Order matters:
#     1. departments (no dependencies)
#     2. employees (depends on departments)
#     3. skills (no dependencies)
#     4. courses (no dependencies)
#     5. course_skills (depends on courses, skills)
#     6. mentorship_profiles (depends on employees)
#     7. marketplace_items (no dependencies)
#     8. goals (depends on employees)
    
#     Args:
#         conn: SQLite database connection
#     """
#     print("\n🌱 Loading seed data...")
#     print("=" * 50)
    
#     try:
#         # Load in correct order (FK dependencies)
#         load_departments(conn)
#         load_employees(conn)
#         load_skills(conn)
#         load_courses(conn)
#         load_course_skills(conn)
#         load_mentorship_profiles(conn)
#         load_marketplace_items(conn)
#         load_goals(conn)
#         load_wellbeing_seeds(conn)
        
#         print("=" * 50)
#         print("✅ All seed data loaded successfully!\n")
        
#     except Exception as e:
#         print(f"❌ Error loading seed data: {e}")
#         conn.rollback()
#         raise


# if __name__ == "__main__":
#     """
#     Run this module directly to seed the database:
    
#         python -m app.data.seed_data
#     """
#     from app.core.db import get_connection, init_db
    
#     print("\n🚀 PSA Hackathon - Database Seeding")
#     print("=" * 50)
    
#     # Get connection and initialize database
#     conn = get_connection()
#     print("📁 Database location:", conn.execute("PRAGMA database_list").fetchone()[2])
    
#     # Create tables if they don't exist
#     print("\n🔧 Initializing database schema...")
#     init_db(conn)
#     print("✅ Database schema initialized")
    
#     # Load all seed data
#     load_all_seeds(conn)
    
#     # Verify data loaded
#     cursor = conn.cursor()
#     stats = {
#         "departments": cursor.execute("SELECT COUNT(*) FROM departments").fetchone()[0],
#         "employees": cursor.execute("SELECT COUNT(*) FROM employees").fetchone()[0],
#         "skills": cursor.execute("SELECT COUNT(*) FROM skills").fetchone()[0],
#         "courses": cursor.execute("SELECT COUNT(*) FROM courses").fetchone()[0],
#         "course_skills": cursor.execute("SELECT COUNT(*) FROM course_skills").fetchone()[0],
#         "mentorship_profiles": cursor.execute("SELECT COUNT(*) FROM mentorship_profiles").fetchone()[0],
#         "marketplace_items": cursor.execute("SELECT COUNT(*) FROM marketplace_items").fetchone()[0],
#         "goals": cursor.execute("SELECT COUNT(*) FROM goals").fetchone()[0],
#     }
    
#     print("\n📊 Database Statistics:")
#     print("=" * 50)
#     for table, count in stats.items():
#         print(f"  {table:.<30} {count:>3} records")
    
#     print("=" * 50)
#     print("✅ Seeding complete! Database ready for use.\n")
    
#     conn.close()

"""
Data Seeding Module + Employee Insights Generation

Usage:
    python seed_data.py
    or
    python -m app.data.seed_data
"""

from __future__ import annotations
import json, sqlite3, sys
from pathlib import Path
from typing import Any
from datetime import datetime

# ========================================
# Path Setup
# ========================================

CURRENT_DIR = Path(__file__).resolve().parent
APP_DIR = CURRENT_DIR.parent
SRC_DIR = APP_DIR.parent

# Ensure src is in sys.path so "app.*" imports work
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# ========================================
# Imports (after path setup)
# ========================================

from app.data.utils.position_level import derive_position_level
from app.core.db import get_connection, init_db
from app.agent.course_recommendation_agent.tools import (
    get_employee_context, recommend_courses_tool, employee_repo
)
from app.agent.course_recommendation_agent.main import (
    get_leadership_potential_employer, get_career_pathway
)

# ========================================
# Utility Functions
# ========================================

def get_seeds_dir() -> Path:
    return CURRENT_DIR / "seeds"

def get_db_path() -> Path:
    db_dir = CURRENT_DIR / "database"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "app.db"

def load_json_file(filepath: Path) -> list[dict[str, Any]]:
    if not filepath.exists():
        print(f"⚠️ Missing seed file: {filepath.name}")
        return []
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

# ========================================
# Seeding Helpers
# ========================================

def load_departments(conn):
    data = load_json_file(get_seeds_dir() / "departments.json")
    c = conn.cursor()
    for r in data:
        c.execute("INSERT OR REPLACE INTO departments (id, name) VALUES (?, ?)", (r["id"], r["name"]))
    conn.commit()
    print(f"✅ Loaded {len(data)} departments")

def load_skills(conn):
    data = load_json_file(get_seeds_dir() / "skills.json")
    c = conn.cursor()
    for r in data:
        c.execute("INSERT OR REPLACE INTO skills (id, name, category) VALUES (?, ?, ?)",
                  (r["id"], r["name"], r["category"]))
    conn.commit()
    print(f"✅ Loaded {len(data)} skills")

def load_employees(conn):
    data = load_json_file(get_seeds_dir() / "employees.json")
    c = conn.cursor()
    for r in data:
        pos_lvl = derive_position_level(r.get("level"), r.get("position_level"))
        c.execute("""
            INSERT OR REPLACE INTO employees
            (id, name, role, department_id, level, position_level,
             points_current, hire_date, skills_map, courses_enrolled_map, goals_set)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["id"], r["name"], r["role"], r["department_id"], r["level"], pos_lvl,
            r["points_current"], r["hire_date"], r["skills_map"],
            r["courses_enrolled_map"], r["goals_set"]
        ))
    conn.commit()
    print(f"✅ Loaded {len(data)} employees")

def load_courses(conn):
    data = load_json_file(get_seeds_dir() / "courses.json")
    c = conn.cursor()
    for r in data:
        c.execute("""
            INSERT OR REPLACE INTO courses
            (id, title, description, difficulty, duration_weeks,
             effort_hours_week, points_reward, roi, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["id"], r["title"], r["description"], r["difficulty"], r["duration_weeks"],
            r["effort_hours_week"], r["points_reward"], r["roi"], r["active"]
        ))
    conn.commit()
    print(f"✅ Loaded {len(data)} courses")

def load_course_skills(conn):
    data = load_json_file(get_seeds_dir() / "course_skills.json")
    c = conn.cursor()
    for r in data:
        c.execute("INSERT OR REPLACE INTO course_skills (course_id, skill_id, weight) VALUES (?, ?, ?)",
                  (r["course_id"], r["skill_id"], r["weight"]))
    conn.commit()
    print(f"✅ Loaded {len(data)} course-skill mappings")

def load_mentorship_profiles(conn):
    data = load_json_file(get_seeds_dir() / "mentorship_profiles.json")
    c = conn.cursor()
    inserted = 0
    for r in data:
        employee_id = r["employee_id"]
        exists = c.execute("SELECT 1 FROM employees WHERE id = ?", (employee_id,)).fetchone()
        if not exists:
            print(f"⚠️ Skipping mentorship profile for missing employee {employee_id}")
            continue
        c.execute("""
            INSERT OR REPLACE INTO mentorship_profiles
            (employee_id, is_mentor, capacity, mentees_count, rating, personality)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            employee_id, r["is_mentor"], r["capacity"],
            r["mentees_count"], r["rating"], r["personality"]
        ))
        inserted += 1
    conn.commit()
    print(f"✅ Loaded {inserted} mentorship profiles")

def load_marketplace_items(conn):
    data = load_json_file(get_seeds_dir() / "marketplace_items.json")
    c = conn.cursor()
    for r in data:
        c.execute("""
            INSERT OR REPLACE INTO marketplace_items
            (id, name, description, points_cost, category, in_stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            r["id"], r["name"], r["description"], r["points_cost"],
            r["category"], r["in_stock"]
        ))
    conn.commit()
    print(f"✅ Loaded {len(data)} marketplace items")

def load_goals(conn):
    data = load_json_file(get_seeds_dir() / "goals.json")
    c = conn.cursor()
    inserted = 0
    for r in data:
        employee_id = r["employee_id"]
        exists = c.execute("SELECT 1 FROM employees WHERE id = ?", (employee_id,)).fetchone()
        if not exists:
            print(f"⚠️ Skipping goal for missing employee {employee_id}")
            continue
        c.execute(
            "INSERT INTO goals (employee_id, title, target_date, progress_percent) VALUES (?, ?, ?, ?)",
            (employee_id, r["title"], r["target_date"], r["progress_percent"]),
        )
        inserted += 1
    conn.commit()
    print(f"✅ Loaded {inserted} goals")

# ========================================
# Employee Insights Generation
# ========================================

def generate_employee_insights(conn):
    print("\n🧠 Checking employee insights table...")
    c = conn.cursor()
    # Ensure table exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS employee_insights (
            id TEXT PRIMARY KEY,
            name TEXT,
            department_id TEXT,
            role TEXT,
            level TEXT,
            years_with_company REAL,
            skills TEXT,
            goals TEXT,
            courses_enrolled TEXT,
            leadership_json TEXT,
            leadership_summary TEXT,
            career_pathway_json TEXT,
            career_pathway_summary TEXT,
            courses_recommended_json TEXT
        )
    """)
    conn.commit()

    # Check if already populated
    c.execute("SELECT COUNT(*) FROM employee_insights")
    existing_count = c.fetchone()[0]

    if existing_count > 0:
        print(f"⚠️ Employee insights already exist ({existing_count} records) — skipping regeneration.")
        return

    print("📋 Generating new employee insights...")
    employees = employee_repo.list_employees()
    if not employees:
        print("⚠️ No employees found — skipping insights generation.")
        return
    print(f"📋 Found {len(employees)} employees")

    for emp in employees:
        emp_id = emp.get("id")
        print(f"→ Processing {emp_id}")
        ctx = get_employee_context(emp_id)
        profile, skills, goals, enrolled = ctx["profile"], ctx["skills"], ctx["goals"], ctx["courses_enrolled"]

        hire_date = datetime.strptime(profile["hire_date"], "%Y-%m-%d")
        years = (datetime.now() - hire_date).days / 365

        leadership = get_leadership_potential_employer(emp_id)
        career = get_career_pathway(emp_id)
        courses = recommend_courses_tool(skills)

        c.execute("""
            INSERT OR REPLACE INTO employee_insights
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            emp_id, profile["name"], profile["department_id"], profile["role"],
            profile["level"], years, json.dumps(skills), json.dumps(goals),
            json.dumps(enrolled), json.dumps(leadership.get("json", {})),
            leadership.get("text_summary", ""), json.dumps(career.get("json", {})),
            career.get("text_summary", ""), json.dumps(courses)
        ))
        conn.commit()
        break

    print("✅ Employee insights generated and saved!")


def load_all_seeds(conn, generate_insights: bool = True):
    print("\n🌱 Loading seed data...")
    print("=" * 60)
    load_departments(conn)
    load_employees(conn)
    load_skills(conn)
    load_courses(conn)
    load_course_skills(conn)
    load_mentorship_profiles(conn)
    load_marketplace_items(conn)
    load_goals(conn)

    if generate_insights:
        # Generate employee insights only if not already generated
        generate_employee_insights(conn)

    print("=" * 60)
    print("✅ All seed data + insights loaded successfully!\n")

# ========================================
# Main Entry
# ========================================

if __name__ == "__main__":
    print("\n🚀 PSA Hackathon - Database Seeding + Insights Generation")
    print("=" * 60)

    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    print(f"📁 Using database: {db_path}")

    print("\n🔧 Initializing schema...")
    init_db(conn)
    print("✅ Schema ready")

    load_all_seeds(conn)

    print("\n📊 Database Summary")
    print("=" * 60)
    c = conn.cursor()
    for table in [
        "departments", "employees", "skills", "courses",
        "course_skills", "mentorship_profiles",
        "marketplace_items", "goals", "employee_insights"
    ]:
        try:
            count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table:<30} {count:>5} rows")
        except sqlite3.Error:
            print(f"{table:<30} (missing table)")
    print("=" * 60)
    print("🎉 All data seeded and verified.")
    conn.close()
