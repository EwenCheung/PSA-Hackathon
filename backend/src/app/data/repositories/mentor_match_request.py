"""Repository for mentor match requests."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .base import BaseRepository


class MentorMatchRequestRepository(BaseRepository):
    """Data access helpers for mentor_match_requests table."""

    TABLE = "mentor_match_requests"
    ID_FIELD = "id"

    def get_request(self, request_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, request_id)

    def list_requests(
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

        query = f"{query} ORDER BY created_at DESC"

        cur = self.conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def create_request(self, data: Dict[str, Any]) -> int:
        return self.create(self.TABLE, data)

    def update_request(self, request_id: int, data: Dict[str, Any]) -> int:
        return self.update(self.TABLE, self.ID_FIELD, request_id, data)

    def delete_request(self, request_id: int) -> int:
        return self.delete(self.TABLE, self.ID_FIELD, request_id)

    @staticmethod
    def decode_payload(raw: Optional[str]) -> Dict[str, Any]:
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return {}

    @staticmethod
    def encode_payload(payload: Dict[str, Any]) -> str:
        return json.dumps(payload)
