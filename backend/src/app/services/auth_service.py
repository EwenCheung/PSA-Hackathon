"""
AuthService: Validates lightweight employee ID login.
"""
from __future__ import annotations

from typing import Optional, Dict, Any
from datetime import datetime, timezone

from app.core.db import get_connection
from app.data.repositories.employee import EmployeeRepository


class AuthService:
    def __init__(self) -> None:
        conn = get_connection()
        self.employee_repo = EmployeeRepository(conn)

    def validate_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """
        Return employee profile summary for a valid ID, otherwise None.
        """
        profile = self.employee_repo.get_employee_profile(employee_id)
        if not profile:
            return None

        return {
            "id": profile.get("id"),
            "name": profile.get("name"),
            "role": profile.get("role"),
            "department_id": profile.get("department_id"),
            "level": profile.get("level"),
            "position_level": profile.get("position_level"),
            "points_current": profile.get("points_current", 0),
            "hire_date": profile.get("hire_date"),
        }

    @staticmethod
    def issue_session_timestamp() -> str:
        """
        Generate an ISO8601 timestamp for session issuance.
        """
        return datetime.now(timezone.utc).isoformat()


auth_service = AuthService()
