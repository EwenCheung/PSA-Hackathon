"""
API: Matching

Purpose
- Surface mentors, mentees, AI-suggested matches and confirm selections.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/matching/mentors
- GET /api/v1/matching/mentees
- GET /api/v1/matching/suggested
- POST /api/v1/matching/confirm
"""

from typing import List
from app.models.pydantic_schemas import MentorshipProfileDetail, MentorshipMatchDetail


EXPECTED_ROUTES: List[str] = [
    "/api/v1/matching/mentors",
    "/api/v1/matching/mentees",
    "/api/v1/matching/suggested",
    "/api/v1/matching/confirm",
]


def list_mentors() -> List[MentorshipProfileDetail]:
    """
    Contract: return mentors with capacity, expertise, rating.
    Returns: List[MentorshipProfileDetail]
    """
    # Placeholder
    raise NotImplementedError


def list_mentees() -> List[MentorshipProfileDetail]:
    """
    Contract: return mentees with goals and personality.
    Returns: List[MentorshipProfileDetail]
    """
    # Placeholder
    raise NotImplementedError


def suggested() -> List[MentorshipMatchDetail]:
    """
    Contract: return suggested pairs with scores and reasons.
    Returns: List[MentorshipMatchDetail]
    """
    # Placeholder
    raise NotImplementedError


def confirm(pairs: List[dict]) -> MentorshipMatchDetail:
    """
    Contract: confirm selected matches and persist state.
    Returns: MentorshipMatchDetail
    """
    # Placeholder
    raise NotImplementedError

