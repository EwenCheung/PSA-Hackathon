"""
API v1: Wellbeing Router

Purpose
- Support anonymous-friendly chat, message history, and sentiment snapshot.
"""
from typing import Optional

from fastapi import APIRouter

from ...agent.well_being_agent.agent import well_being_agent
from pydantic import BaseModel, Field, AliasChoices

class WellbeingMessageRequest(BaseModel):
    message: str
    is_anonymous: bool = Field(
        default=False,
        validation_alias=AliasChoices("is_anonymous", "isAnonymous"),
    )
    anon_session_id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("anon_session_id", "anonSessionId"),
    )

    model_config = {"populate_by_name": True}

router = APIRouter(
    prefix="/api/v1/wellbeing",
    tags=["Wellbeing"],
)


@router.get("/{employee_id}/messages_past_10_history")
async def get_messages(employee_id: str):
    return well_being_agent.get_messages(employee_id)


@router.post("/{employee_id}/messages")
async def post_message(employee_id: str, req: WellbeingMessageRequest):
    return well_being_agent.post_message(employee_id, req)
