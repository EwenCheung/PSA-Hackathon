"""
DepartmentRepository: Data access for departments table.
"""
from .base import BaseRepository
from typing import Optional, List

class DepartmentRepository(BaseRepository):
    TABLE = "departments"
    ID_FIELD = "id"

    def get_department(self, department_id: str) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, department_id)

    def list_departments(self) -> List[dict]:
        return self.list_all(self.TABLE)
