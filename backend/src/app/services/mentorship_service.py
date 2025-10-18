"""
MentorshipService: Business logic for mentorship domain.
"""
from app.data.repositories.mentorship_profile import MentorshipProfileRepository
from app.data.repositories.mentorship_match import MentorshipMatchRepository
from app.data.repositories.mentor_session import MentorSessionRepository
from app.data.repositories.employee import EmployeeRepository
from app.models.pydantic_schemas import MentorshipProfileDetail, MentorshipMatchDetail
from app.core.db import get_connection
from typing import List

class MentorshipService:
    def __init__(self):
        conn = get_connection()
        self.profile_repo = MentorshipProfileRepository(conn)
        self.match_repo = MentorshipMatchRepository(conn)
        self.session_repo = MentorSessionRepository(conn)
        self.employee_repo = EmployeeRepository(conn)

    def get_available_mentors(self, available_only: bool = True) -> List[MentorshipProfileDetail]:
        profiles = self.profile_repo.list_profiles()
        filtered = [MentorshipProfileDetail(**p) for p in profiles if not available_only or p.get("capacity", 0) > p.get("mentees_count", 0)]
        return filtered

    def get_mentee_candidates(self) -> List[dict]:
        employees = self.employee_repo.list_employees()
        return [e for e in employees if e.get("role") == "mentee"]

    def calculate_match_score(self, mentor_id: str, mentee_id: str) -> float:
        # Placeholder: returns 1.0
        return 1.0

    def generate_match_suggestions(self, limit: int = 5) -> List[MentorshipMatchDetail]:
        matches = self.match_repo.list_matches()[:limit]
        return [MentorshipMatchDetail(**m) for m in matches]

    def confirm_match(self, match_id: int) -> MentorshipMatchDetail:
        self.match_repo.update(self.match_repo.TABLE, self.match_repo.ID_FIELD, match_id, {"status": "confirmed"})
        match = self.match_repo.get_match(match_id)
        return MentorshipMatchDetail(**match)

    def record_session(self, mentor_id: str, mentee_id: str, session_data: dict) -> dict:
        session_data["mentor_id"] = mentor_id
        session_data["mentee_id"] = mentee_id
        session_id = self.session_repo.create(self.session_repo.TABLE, session_data)
        return self.session_repo.get_session(session_id)

    def award_mentor_points(self, mentor_id: str, points: int) -> dict:
        # Placeholder: no-op
        return {"mentor_id": mentor_id, "points": points}
