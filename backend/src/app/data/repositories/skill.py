"""
SkillRepository: Data access for skills table.
"""
from .base import BaseRepository
from typing import Optional, List

class SkillRepository(BaseRepository):
    TABLE = "skills"
    ID_FIELD = "id"

    def get_skill(self, skill_id: str) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, skill_id)

    def list_skills(self) -> List[dict]:
        return self.list_all(self.TABLE)
