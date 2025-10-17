"""
API: Auth (ID-only)

Purpose
- Accept `employee_id` and validate existence. No signup, no password.

Routes (contracts only; implemented later via FastAPI):
- POST /api/v1/auth/login
"""
from typing import Dict, List


EXPECTED_ROUTES: List[str] = [
    "/api/v1/auth/login",
]


def login(employee_id: str) -> Dict:
    """Contract: validate employee id and return employee profile."""
    raise NotImplementedError

