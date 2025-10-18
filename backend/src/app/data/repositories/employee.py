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
