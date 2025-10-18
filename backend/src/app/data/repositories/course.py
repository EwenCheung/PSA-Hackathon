"""
CourseRepository: Data access for courses table.
"""
from .base import BaseRepository
from typing import Optional, List

class CourseRepository(BaseRepository):
    TABLE = "courses"
    ID_FIELD = "id"

    def get_course(self, course_id: str) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, course_id)

    def list_courses(self) -> List[dict]:
        return self.list_all(self.TABLE)
