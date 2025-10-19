import json
from typing import Optional, List, Dict, Any
from pathlib import Path
from .base import BaseRepository
import sqlite3


JSON_FILE = Path(__file__).parent.parent / "seeds" / "employees.json"

class EmployeeRepository(BaseRepository):
    TABLE = "employees"
    ID_FIELD = "id"

    def __init__(self, conn, auto_sync: bool = True):
        super().__init__(conn)
        self.conn.row_factory = sqlite3.Row
        if auto_sync:
            self.sync_from_json()

    # ---------- JSON Parsing Helpers ----------
    def _parse_json_field(self, value: Optional[str], default):
        if not value:
            return default
        try:
            return json.loads(value)
        except (ValueError, TypeError, json.JSONDecodeError):
            return default

    def _normalize_employee(self, row: dict) -> dict:
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
        row = self.get_by_id(self.TABLE, self.ID_FIELD, employee_id)
        return self._normalize_employee(row) if row else None

    def list_employees(self) -> List[dict]:
        rows = self.list_all(self.TABLE)
        return [self._normalize_employee(row) for row in rows if row]

    # ---------- Specific Getters ----------
    def get_employee_skills(self, employee_id: str) -> Dict[str, Any]:
        emp = self.get_employee(employee_id)
        return emp.get("skills", {}) if emp else {}

    def get_employee_goals(self, employee_id: str) -> List[str]:
        emp = self.get_employee(employee_id)
        return emp.get("goals", []) if emp else []

    def get_employee_courses(self, employee_id: str) -> Dict[str, Any]:
        emp = self.get_employee(employee_id)
        return emp.get("courses_enrolled", {}) if emp else {}

    def get_employee_profile(self, employee_id: str) -> Dict[str, Any]:
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

    # ---------- Sync from JSON ----------
    def sync_from_json(self):
        """Load employees.json and sync the employees table."""
        if not JSON_FILE.exists():
            print(f"Warning: {JSON_FILE} does not exist.")
            return

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            employees = json.load(f)

        cur = self.conn.cursor()

        # Drop existing table
        cur.execute(f"DROP TABLE IF EXISTS {self.TABLE}")

        # Create fresh employees table
        cur.execute(f"""
            CREATE TABLE {self.TABLE} (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT,
                department_id TEXT,
                level TEXT,
                points_current INTEGER DEFAULT 0,
                hire_date TEXT,
                skills_map TEXT,
                courses_enrolled_map TEXT,
                goals_set TEXT
            )
        """)
        self.conn.commit()

        # Insert data
        query = f"""
            INSERT INTO {self.TABLE}
            (id, name, role, department_id, level, points_current, hire_date, skills_map, courses_enrolled_map, goals_set)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = [
            (
                e["id"],
                e["name"],
                e.get("role"),
                e.get("department_id"),
                e.get("level"),
                e.get("points_current", 0),
                e.get("hire_date"),
                json.dumps(e.get("skills_map", {})),
                json.dumps(e.get("courses_enrolled_map", {})),
                json.dumps(e.get("goals_set", []))
            )
            for e in employees
        ]
        cur.executemany(query, data)
        self.conn.commit()
        print(f"Synced {len(data)} employees from JSON into {self.TABLE}.")
