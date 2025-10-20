"""
MentorshipMatchRepository: Data access for mentorship_matches table.
"""
from .base import BaseRepository
from typing import Optional, List, Dict, Any

class MentorshipMatchRepository(BaseRepository):
    TABLE = "mentorship_matches"
    ID_FIELD = "id"

    def get_match(self, match_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, match_id)

    def list_matches(self) -> List[dict]:
        return self.list_all(self.TABLE)

    def list_matches_filtered(
        self,
        mentor_id: Optional[str] = None,
        mentee_id: Optional[str] = None,
    ) -> List[dict]:
        query = f"SELECT * FROM {self.TABLE}"
        params: List[Any] = []
        clauses: List[str] = []

        if mentor_id:
            clauses.append("mentor_id = ?")
            params.append(mentor_id)

        if mentee_id:
            clauses.append("mentee_id = ?")
            params.append(mentee_id)

        if clauses:
            query = f"{query} WHERE {' AND '.join(clauses)}"

        cur = self.conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def create_match(self, data: Dict[str, Any]) -> int:
        return self.create(self.TABLE, data)
