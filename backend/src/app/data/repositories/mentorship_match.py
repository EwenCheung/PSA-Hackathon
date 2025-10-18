"""
MentorshipMatchRepository: Data access for mentorship_matches table.
"""
from .base import BaseRepository
from typing import Optional, List

class MentorshipMatchRepository(BaseRepository):
    TABLE = "mentorship_matches"
    ID_FIELD = "id"

    def get_match(self, match_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, match_id)

    def list_matches(self) -> List[dict]:
        return self.list_all(self.TABLE)
