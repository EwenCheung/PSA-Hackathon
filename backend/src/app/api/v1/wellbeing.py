"""
API: Wellbeing

Purpose
- Support anonymous-friendly chat, message history, and sentiment snapshot.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/wellbeing/{employee_id}/messages
- POST /api/v1/wellbeing/{employee_id}/messages
- GET /api/v1/wellbeing/{employee_id}/sentiment
"""
from typing import Dict, List


EXPECTED_ROUTES: List[str] = [
    "/api/v1/wellbeing/{employee_id}/messages",
    "/api/v1/wellbeing/{employee_id}/sentiment",
]


def list_messages(employee_id: str) -> List[Dict]:
    """Contract: return message history for employee."""
    raise NotImplementedError


def post_message(employee_id: str, content: str, is_anonymous: bool = False) -> Dict:
    """Contract: record user message and return AI response."""
    raise NotImplementedError


def get_sentiment(employee_id: str) -> Dict:
    """Contract: return latest sentiment label and trend."""
    raise NotImplementedError

