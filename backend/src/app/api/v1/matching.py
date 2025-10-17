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
from typing import Dict, List


EXPECTED_ROUTES: List[str] = [
    "/api/v1/matching/mentors",
    "/api/v1/matching/mentees",
    "/api/v1/matching/suggested",
    "/api/v1/matching/confirm",
]


def list_mentors() -> List[Dict]:
    """Contract: return mentors with capacity, expertise, rating."""
    raise NotImplementedError


def list_mentees() -> List[Dict]:
    """Contract: return mentees with goals and personality."""
    raise NotImplementedError


def suggested() -> List[Dict]:
    """Contract: return suggested pairs with scores and reasons."""
    raise NotImplementedError


def confirm(pairs: List[Dict]) -> Dict:
    """Contract: confirm selected matches and persist state."""
    raise NotImplementedError

