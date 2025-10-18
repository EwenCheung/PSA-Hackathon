"""
API: Wellbeing

Purpose
- Support anonymous-friendly chat, message history, and sentiment snapshot.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/wellbeing/{employee_id}/messages
- POST /api/v1/wellbeing/{employee_id}/messages
- GET /api/v1/wellbeing/{employee_id}/sentiment
"""

from typing import List
from app.models.pydantic_schemas import WellbeingMessageDetail, SentimentSnapshotDetail


EXPECTED_ROUTES: List[str] = [
    "/api/v1/wellbeing/{employee_id}/messages",
    "/api/v1/wellbeing/{employee_id}/sentiment",
]


def list_messages(employee_id: str) -> List[WellbeingMessageDetail]:
    """
    Contract: return message history for employee.
    Returns: List[WellbeingMessageDetail]
    """
    # Placeholder
    raise NotImplementedError


def post_message(employee_id: str, content: str, is_anonymous: bool = False) -> WellbeingMessageDetail:
    """
    Contract: record user message and return AI response.
    Returns: WellbeingMessageDetail
    """
    # Placeholder
    raise NotImplementedError


def get_sentiment(employee_id: str) -> SentimentSnapshotDetail:
    """
    Contract: return latest sentiment label and trend.
    Returns: SentimentSnapshotDetail
    """
    # Placeholder
    raise NotImplementedError

