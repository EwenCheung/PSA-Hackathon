"""
API: Analytics

Purpose
- Company-wide KPIs and aggregates for employer dashboard.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/analytics/overview
- GET /api/v1/analytics/departments
- GET /api/v1/analytics/employees
"""

from typing import List
from app.models.pydantic_schemas import DepartmentDetail, EmployeeDetail


EXPECTED_ROUTES: List[str] = [
    "/api/v1/analytics/overview",
    "/api/v1/analytics/departments",
    "/api/v1/analytics/employees",
]


def overview() -> dict:
    """
    Contract: return top-level KPIs for dashboard tiles.
    Returns: dict (placeholder)
    """
    # Placeholder
    raise NotImplementedError


def departments() -> List[DepartmentDetail]:
    """
    Contract: return department aggregates including sentiment.
    Returns: List[DepartmentDetail]
    """
    # Placeholder
    raise NotImplementedError


def employees() -> List[EmployeeDetail]:
    """
    Contract: return employee rows for detailed cards.
    Returns: List[EmployeeDetail]
    """
    # Placeholder
    raise NotImplementedError

