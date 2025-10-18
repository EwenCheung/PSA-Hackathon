"""
MentorshipProfileRepository: Data access for mentorship_profiles table.
"""
from .base import BaseRepository
from typing import Optional, List

class MentorshipProfileRepository(BaseRepository):
    TABLE = "mentorship_profiles"
    ID_FIELD = "employee_id"

    def get_profile(self, employee_id: str) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, employee_id)

    def list_profiles(self) -> List[dict]:
        return self.list_all(self.TABLE)
