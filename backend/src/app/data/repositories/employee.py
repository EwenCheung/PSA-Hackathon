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

    # Add custom employee queries as needed
