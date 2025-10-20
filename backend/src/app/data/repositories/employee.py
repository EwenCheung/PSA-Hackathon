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
            "position_level": row.get("position_level"),
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
            "position_level": emp.get("position_level"),
            "department_id": emp["department_id"],
            "points_current": emp["points_current"],
            "hire_date": emp["hire_date"],
        }

    # ---------- Sync from JSON ----------
    # def sync_from_json(self):
    #     """Load employees.json and sync the employees table."""
    #     if not JSON_FILE.exists():
    #         print(f"Warning: {JSON_FILE} does not exist.")
    #         return

    #     with open(JSON_FILE, "r", encoding="utf-8") as f:
    #         employees = json.load(f)

    #     cur = self.conn.cursor()

    #     # Drop existing table
    #     cur.execute(f"DROP TABLE IF EXISTS {self.TABLE}")

    #     # Create fresh employees table
    #     cur.execute(f"""
    #         CREATE TABLE {self.TABLE} (
    #             id TEXT PRIMARY KEY,
    #             name TEXT NOT NULL,
    #             role TEXT,
    #             department_id TEXT,
    #             level TEXT,
    #             points_current INTEGER DEFAULT 0,
    #             hire_date TEXT,
    #             skills_map TEXT,
    #             courses_enrolled_map TEXT,
    #             goals_set TEXT
    #         )
    #     """)
    #     self.conn.commit()

    #     # Insert data
    #     query = f"""
    #         INSERT INTO {self.TABLE}
    #         (id, name, role, department_id, level, points_current, hire_date, skills_map, courses_enrolled_map, goals_set)
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     """
    #     data = [
    #         (
    #             e["id"],
    #             e["name"],
    #             e.get("role"),
    #             e.get("department_id"),
    #             e.get("level"),
    #             e.get("points_current", 0),
    #             e.get("hire_date"),
    #             json.dumps(e.get("skills_map", {})),
    #             json.dumps(e.get("courses_enrolled_map", {})),
    #             json.dumps(e.get("goals_set", []))
    #         )
    #         for e in employees
    #     ]
    #     cur.executemany(query, data)
    #     self.conn.commit()
    #     print(f"Synced {len(data)} employees from JSON into {self.TABLE}.")

    def find_employees_by_skills(self, skills: List[str]) -> List[dict]:
        """
        Find employees who have any of the specified skills.
        
        Args:
            skills: List of skill IDs to search for
        
        Returns:
            List of employee records matching any of the skills
        """
        if not skills:
            return []
        
        cur = self.conn.cursor()
        
        # Build OR conditions for each skill
        conditions = [f'skills_map LIKE ?' for _ in skills]
        where_clause = ' OR '.join(conditions)
        
        query = f"""
            SELECT * FROM {self.TABLE}
            WHERE {where_clause}
        """
        
        # Create LIKE patterns for each skill
        params = [f'%"{skill}"%' for skill in skills]
        
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    
    def get_employees_by_department(self, department_id: str) -> List[dict]:
        """
        Get all employees in a specific department.
        
        Args:
            department_id: The department ID to filter by
        
        Returns:
            List of employees in the department
        """
        cur = self.conn.cursor()
        cur.execute(
            f"SELECT * FROM {self.TABLE} WHERE department_id = ?",
            (department_id,)
        )
        rows = cur.fetchall()
        return [dict(row) for row in rows]