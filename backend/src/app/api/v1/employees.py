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
from typing import Dict, List


EXPECTED_ROUTES: List[str] = [
    "/api/v1/employees/{employee_id}",
    "/api/v1/employees/{employee_id}/career/recommendations",
    "/api/v1/employees/{employee_id}/career/courses/{course_id}/start",
    "/api/v1/employees/{employee_id}/career/courses/{course_id}/complete",
    "/api/v1/employees/{employee_id}/goals",
    "/api/v1/employees/{employee_id}/points",
]


def get_employee_profile(employee_id: str) -> Dict:
    """Contract: return employee profile with points and metadata."""
    raise NotImplementedError


def get_career_recommendations(employee_id: str) -> List[Dict]:
    """Contract: return ranked courses for given employee id."""
    raise NotImplementedError


def start_course(employee_id: str, course_id: str) -> Dict:
    """Contract: mark a course as in-progress for employee."""
    raise NotImplementedError


def complete_course(employee_id: str, course_id: str) -> Dict:
    """Contract: mark a course as completed and add points."""
    raise NotImplementedError


def get_goals(employee_id: str) -> List[Dict]:
    """Contract: return employee career goals with progress and targets."""
    raise NotImplementedError


def adjust_points(employee_id: str, delta: int) -> Dict:
    """Contract: adjust employee points (earn/redeem)."""
    raise NotImplementedError

