"""
EmployeeRepository: Data access for employees table.
"""
from .base import BaseRepository
from typing import Optional, List


class EmployeeRepository(BaseRepository):
    TABLE = "employees"
    ID_FIELD = "id"

    def get_employee(self, employee_id: str) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, employee_id)

    def list_employees(self) -> List[dict]:
        return self.list_all(self.TABLE)

    def count_employees(self) -> int:
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) AS total FROM {self.TABLE}")
        row = cur.fetchone()
        return row["total"] if row else 0

    def list_with_department(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT 
                e.id,
                e.name,
                e.role,
                e.department_id,
                d.name AS department_name,
                e.points_current,
                e.level
            FROM employees e
            LEFT JOIN departments d ON d.id = e.department_id
            ORDER BY e.name
            """
        )
        return [dict(row) for row in cur.fetchall()]

    def get_department_counts(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT 
                e.department_id,
                d.name AS department_name,
                COUNT(*) AS employee_count
            FROM employees e
            LEFT JOIN departments d ON d.id = e.department_id
            GROUP BY e.department_id
            ORDER BY employee_count DESC
            """
        )
        return [dict(row) for row in cur.fetchall()]

    def get_max_points(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COALESCE(MAX(points_current), 0) AS max_points FROM employees")
        row = cur.fetchone()
        return row["max_points"] if row else 0
