# info_for_employer.py
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Add project root to sys.path if needed
import sys
sys.path.insert(0, str(Path(__file__).parents[1]))

# Import helper functions
from tools import (
    get_employee_context,
    recommend_courses_tool,
    employee_repo
)
from main import (
    get_leadership_potential_employer,
    get_career_pathway
)

# -----------------------------
# SQLite DB connection setup
# -----------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "database" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure folders exist

print(f"Using DB path: {DB_PATH}")  # ✅ Debug line

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

# -----------------------------
# Create table (if not exists)
# -----------------------------
cursor.execute("""
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

# -----------------------------
# Fetch all employees
# -----------------------------
all_employees = employee_repo.list_employees()
print(f"Found {len(all_employees)} employees")

for emp in all_employees:
    emp_id = emp.get("id")
    print(f"\n=== Processing Employee {emp_id} ===")

    # --- Employee context ---
    context = get_employee_context(emp_id)
    profile = context["profile"]
    skills = context["skills"]
    goals = context["goals"]
    courses_enrolled = context["courses_enrolled"]

    # --- Years with company ---
    hire_date = datetime.strptime(profile["hire_date"], "%Y-%m-%d")
    years_with_company = (datetime.now() - hire_date).days / 365

    # --- Leadership potential ---
    leadership = get_leadership_potential_employer(emp_id)
    leadership_json = json.dumps(leadership.get("json", {}))
    leadership_summary = leadership.get("text_summary", "")

    # --- Career pathway ---
    career = get_career_pathway(emp_id)
    career_pathway_json = json.dumps(career.get("json", {}))
    career_pathway_summary = career.get("text_summary", "")

    # --- Course recommendations ---
    courses = recommend_courses_tool(skills)
    courses_json = json.dumps(courses)

    # --- Insert / replace into DB ---
    cursor.execute("""
        INSERT OR REPLACE INTO employee_insights (
            id, name, department_id, role, level, years_with_company,
            skills, goals, courses_enrolled,
            leadership_json, leadership_summary,
            career_pathway_json, career_pathway_summary,
            courses_recommended_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        emp_id,
        profile.get("name"),
        profile.get("department_id"),
        profile.get("role"),
        profile.get("level"),
        years_with_company,
        json.dumps(skills),
        json.dumps(goals),
        json.dumps(courses_enrolled),
        leadership_json,
        leadership_summary,
        career_pathway_json,
        career_pathway_summary,
        courses_json
    ))
    conn.commit()

print("\n✅ All employee insights saved to 'employee_insights' table!")
conn.close()
