"""
API: Employees

Purpose
- Employee profile, goals, points and career course lifecycle.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/employees/{employee_id}
- GET /api/v1/employees/{employee_id}/career/recommendations
- POST /api/v1/employees/{employee_id}/career/courses/{course_id}/start
- POST /api/v1/employees/{employee_id}/career/courses/{course_id}/complete
- GET /api/v1/employees/{employee_id}/goals
- PATCH /api/v1/employees/{employee_id}/points
"""

from typing import List

from app.models.pydantic_schemas import EmployeeDetail, CourseDetail, GoalDetail
from app.core.db import get_connection
from app.data.repositories.employee import EmployeeRepository


EXPECTED_ROUTES: List[str] = [
    "/api/v1/employees/{employee_id}",
    "/api/v1/employees/{employee_id}/career/recommendations",
    "/api/v1/employees/{employee_id}/career/courses/{course_id}/start",
    "/api/v1/employees/{employee_id}/career/courses/{course_id}/complete",
    "/api/v1/employees/{employee_id}/goals",
    "/api/v1/employees/{employee_id}/points",
]


def get_employee_profile(employee_id: str) -> EmployeeDetail:
    """
    Contract: return employee profile with points and metadata.
    Returns: EmployeeDetail
    """
    conn = get_connection()
    repo = EmployeeRepository(conn)
    employee = repo.get_employee(employee_id)
    if not employee:
        raise ValueError(f"Employee {employee_id} not found")
    # Convert dict to EmployeeDetail (Pydantic)
    return EmployeeDetail(**employee)


def get_career_recommendations(employee_id: str) -> List[CourseDetail]:
    """
    Contract: return ranked courses for given employee id.
    Returns: List[CourseDetail]
    """
    # Placeholder
    raise NotImplementedError


def start_course(employee_id: str, course_id: str) -> CourseDetail:
    """
    Contract: mark a course as in-progress for employee.
    Returns: CourseDetail
    """
    # Placeholder
    raise NotImplementedError


def complete_course(employee_id: str, course_id: str) -> CourseDetail:
    """
    Contract: mark a course as completed and add points.
    Returns: CourseDetail
    """
    # Placeholder
    raise NotImplementedError


def get_goals(employee_id: str) -> List[GoalDetail]:
    """
    Contract: return employee career goals with progress and targets.
    Returns: List[GoalDetail]
    """
    # Placeholder
    raise NotImplementedError


def adjust_points(employee_id: str, delta: int) -> EmployeeDetail:
    """
    Contract: adjust employee points (earn/redeem).
    Returns: EmployeeDetail
    """
    # Placeholder
    raise NotImplementedError

