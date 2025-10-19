import json
from typing import Optional, List, Dict, Any
from .base import BaseRepository

class EmployeeRepository(BaseRepository):
    TABLE = "employees"
    ID_FIELD = "id"

    # ---------- Utility Methods ----------
    def _parse_json_field(self, value: Optional[str], default):
        """Safely parse JSON field; return default if invalid or empty."""
        if not value:
            return default
        try:
            return json.loads(value)
        except (ValueError, TypeError, json.JSONDecodeError):
            return default

    def _normalize_employee(self, row: dict) -> dict:
        """Convert DB row into a structured dict with parsed fields."""
        if not row:
            return {}

        return {
            "id": row.get("id"),
            "name": row.get("name"),
            "role": row.get("role"),
            "department_id": row.get("department_id"),
            "level": row.get("level"),
            "points_current": row.get("points_current", 0),
            "hire_date": row.get("hire_date"),
            "skills": self._parse_json_field(row.get("skills_map"), {}),
            "courses_enrolled": self._parse_json_field(row.get("courses_enrolled_map"), {}),
            "goals": self._parse_json_field(row.get("goals_set"), []),
        }

    # ---------- Core Data Access ----------
    def get_employee(self, employee_id: str) -> Optional[dict]:
        """Get and normalize a single employee."""
        row = self.get_by_id(self.TABLE, self.ID_FIELD, employee_id)
        return self._normalize_employee(row) if row else None

    def list_employees(self) -> List[dict]:
        """List all employees with normalized data."""
        rows = self.list_all(self.TABLE)
        return [self._normalize_employee(row) for row in rows if row]

    # ---------- Specific Getters ----------
    def get_employee_skills(self, employee_id: str) -> Dict[str, Any]:
        """Return only the employee's skills dictionary."""
        emp = self.get_employee(employee_id)
        return emp.get("skills", {}) if emp else {}

    def get_employee_goals(self, employee_id: str) -> List[str]:
        """Return the employee's goals list."""
        emp = self.get_employee(employee_id)
        return emp.get("goals", []) if emp else []

    def get_employee_courses(self, employee_id: str) -> Dict[str, Any]:
        """Return the employee's enrolled courses dictionary."""
        emp = self.get_employee(employee_id)
        return emp.get("courses_enrolled", {}) if emp else {}

    def get_employee_profile(self, employee_id: str) -> Dict[str, Any]:
        """Return a lightweight profile (non-nested info)."""
        emp = self.get_employee(employee_id)
        if not emp:
            return {}
        return {
            "id": emp["id"],
            "name": emp["name"],
            "role": emp["role"],
            "level": emp["level"],
            "department_id": emp["department_id"],
            "points_current": emp["points_current"],
            "hire_date": emp["hire_date"],
        }
