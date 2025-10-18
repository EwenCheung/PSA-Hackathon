"""
API v1: Wellbeing Router

Purpose
- Support anonymous-friendly chat, message history, and sentiment snapshot.

Routes:
- GET /api/v1/wellbeing/{employee_id}/messages
- POST /api/v1/wellbeing/{employee_id}/messages
- GET /api/v1/wellbeing/{employee_id}/sentiment
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.pydantic_schemas import (
    WellbeingMessageDetail,
    WellbeingMessageCreate,
    SentimentSnapshotDetail
)

# Create router
router = APIRouter(
    prefix="/api/v1/wellbeing",
    tags=["Wellbeing"],
)


@router.get("/{employee_id}/messages", response_model=List[WellbeingMessageDetail])
async def list_messages(employee_id: str):
    """
    Get message history for employee.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        List[WellbeingMessageDetail]: Message history for employee
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Message list not yet implemented"
    )


@router.post("/{employee_id}/messages", response_model=WellbeingMessageDetail)
async def post_message(employee_id: str, message: WellbeingMessageCreate):
    """
    Record user message and return AI response.
    
    Args:
        employee_id: The employee's unique identifier
        message: Message content and anonymity flag
        
    Returns:
        WellbeingMessageDetail: The AI response message
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Message posting not yet implemented"
    )


@router.get("/{employee_id}/sentiment", response_model=SentimentSnapshotDetail)
async def get_sentiment(employee_id: str):
    """
    Get latest sentiment label and trend.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        SentimentSnapshotDetail: Latest sentiment analysis and trend
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Sentiment analysis not yet implemented"
    )

