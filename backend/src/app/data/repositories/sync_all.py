# repositories/sync_all.py
import sqlite3
from pathlib import Path
from .course_skill import CourseSkillRepository
from .course import CourseRepository
from .employee import EmployeeRepository  # <-- added

def sync_all():
    db_path = Path(__file__).parent.parent / "database" / "app.db"
    conn = sqlite3.connect(db_path)
    
    # Sync courses
    course_repo = CourseRepository(conn, auto_sync=False)
    course_repo.sync_from_json()
    
    # Sync course_skills
    course_skill_repo = CourseSkillRepository(conn, auto_sync=False)
    course_skill_repo.sync_from_json()
    
    # Sync employees
    employee_repo = EmployeeRepository(conn, auto_sync=False)
    employee_repo.sync_from_json()
    
    conn.close()
    print("All data synced successfully!")

if __name__ == "__main__":
    sync_all()


# run python -m repositories.sync_all in terminal