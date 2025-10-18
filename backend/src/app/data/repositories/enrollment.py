"""
EnrollmentRepository: Data access for enrollments table.
"""
from .base import BaseRepository
from typing import List

class EnrollmentRepository(BaseRepository):
    TABLE = "enrollments"

    def list_enrollments(self) -> List[dict]:
        return self.list_all(self.TABLE)
