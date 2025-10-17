"""
API: Analytics

Purpose
- Company-wide KPIs and aggregates for employer dashboard.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/analytics/overview
- GET /api/v1/analytics/departments
- GET /api/v1/analytics/employees
"""
from typing import Dict, List


EXPECTED_ROUTES: List[str] = [
    "/api/v1/analytics/overview",
    "/api/v1/analytics/departments",
    "/api/v1/analytics/employees",
]


def overview() -> Dict:
    """Contract: return top-level KPIs for dashboard tiles."""
    raise NotImplementedError


def departments() -> List[Dict]:
    """Contract: return department aggregates including sentiment."""
    raise NotImplementedError


def employees() -> List[Dict]:
    """Contract: return employee rows for detailed cards."""
    raise NotImplementedError

