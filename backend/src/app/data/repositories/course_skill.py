"""
CourseSkillRepository: Data access for course_skills table.
"""
from .base import BaseRepository
from typing import List

class CourseSkillRepository(BaseRepository):
    TABLE = "course_skills"

    def list_course_skills(self) -> List[dict]:
        return self.list_all(self.TABLE)
