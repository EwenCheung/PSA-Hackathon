"""
CourseService: Business logic for course domain.
"""
from app.data.repositories.course import CourseRepository
from app.data.repositories.enrollment import EnrollmentRepository
from app.data.repositories.goal import GoalRepository
from app.models.pydantic_schemas import CourseDetail, GoalDetail
from app.core.db import get_connection
from typing import List

class CourseService:
    def __init__(self):
        conn = get_connection()
        self.course_repo = CourseRepository(conn)
        self.enrollment_repo = EnrollmentRepository(conn)
        self.goal_repo = GoalRepository(conn)

    def get_course_catalog(self, filters=None) -> List[CourseDetail]:
        courses = self.course_repo.list_courses()
        # Apply filters if needed
        return [CourseDetail(**c) for c in courses]

    def get_course_recommendations(self, employee_id: str, limit: int = 5) -> List[CourseDetail]:
        # Placeholder: return top N courses
        courses = self.course_repo.list_courses()[:limit]
        return [CourseDetail(**c) for c in courses]

    def enroll_in_course(self, employee_id: str, course_id: str) -> dict:
        data = {"employee_id": employee_id, "course_id": course_id, "status": "in-progress", "progress_percent": 0}
        self.enrollment_repo.create(self.enrollment_repo.TABLE, data)
        return data

    def update_course_progress(self, employee_id: str, course_id: str, progress: int) -> dict:
        self.enrollment_repo.update(self.enrollment_repo.TABLE, "employee_id", employee_id, {"progress_percent": progress})
        return {"employee_id": employee_id, "course_id": course_id, "progress_percent": progress}

    def complete_course(self, employee_id: str, course_id: str) -> dict:
        self.enrollment_repo.update(self.enrollment_repo.TABLE, "employee_id", employee_id, {"status": "completed", "progress_percent": 100})
        return {"employee_id": employee_id, "course_id": course_id, "status": "completed", "progress_percent": 100}

    def calculate_course_score(self, course: dict, employee_skills: List[str]) -> float:
        # Placeholder: simple skill match count
        return float(len(set(course.get("skills", [])) & set(employee_skills)))
