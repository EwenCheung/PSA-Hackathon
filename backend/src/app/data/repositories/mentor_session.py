"""
MentorSessionRepository: Data access for mentor_sessions table.
"""
from .base import BaseRepository
from typing import Optional, List

class MentorSessionRepository(BaseRepository):
    TABLE = "mentor_sessions"
    ID_FIELD = "id"

    def get_session(self, session_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, session_id)

    def list_sessions(self) -> List[dict]:
        return self.list_all(self.TABLE)
