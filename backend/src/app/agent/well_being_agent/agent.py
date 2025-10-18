from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, List, Optional

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

from app.core.config import settings
from .system_prompt import SYSTEM_PROMPT
# from .tools import _

load_dotenv()
_ = settings  # ensure env loaded

FALLBACK_MESSAGE = "Message failed to send, please try again."


class WellBeingAgent:
    def __init__(self) -> None:
        self.agent = None
        self.user_histories: dict[str, list[dict[str, Any]]] = {}

    def create_wellbeing_agent(self) -> None:
        deployment = os.getenv("DEPLOYMENT")
        api_version = os.getenv("API_VERSION")

        llm = AzureChatOpenAI(
            azure_deployment=deployment,
            api_version=api_version,
            temperature=0.7,
            max_tokens=256,
        )

        # create_agent signature may vary by langchain version.
        # Expecting an agent that takes {"messages": List[BaseMessage]}.
        from langchain.agents import create_agent

        self.agent = create_agent(
            model=llm,
            tools=[],
            system_prompt=SYSTEM_PROMPT,
        )

    def _extract_ai(self, result: Any) -> Optional[AIMessage]:
        if isinstance(result, AIMessage):
            return result
        if isinstance(result, dict):
            msgs = result.get("messages")
            if isinstance(msgs, list):
                for m in reversed(msgs):
                    if isinstance(m, AIMessage):
                        return m
                    if isinstance(m, dict) and m.get("type") == "ai":
                        return AIMessage(content=m.get("content", ""))
        return None

    def _to_langchain_messages(self, entries: List[dict[str, Any]]) -> List[BaseMessage]:
        messages: List[BaseMessage] = []
        for entry in entries:
            sender = entry.get("sender")
            content = entry.get("content", "")
            if sender == "user":
                messages.append(HumanMessage(content=content))
            elif sender == "ai":
                messages.append(AIMessage(content=content))
        return messages

    def _make_entry(
        self,
        *,
        sender: str,
        content: str,
        is_anonymous: bool = False,
        anon_session_id: Optional[str] = None,
    ) -> dict[str, Any]:
        return {
            "sender": sender,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "is_anonymous": is_anonymous,
            "anon_session_id": anon_session_id,
        }

    def _persist_history(self, employee_id: str, entry: dict[str, Any]) -> None:
        history = self.user_histories.setdefault(employee_id, [])
        history.append(entry)
        if len(history) > 20:
            self.user_histories[employee_id] = history[-20:]

    def get_messages(self, employee_id: str) -> list[dict[str, Any]]:
        history = self.user_histories.get(employee_id, [])
        return history[-10:]

    def get_message(self, employee_id: str) -> list[dict[str, Any]]:
        return self.get_messages(employee_id)

    def post_message(self, employee_id: str, req) -> dict:
        if self.agent is None:
            self.create_wellbeing_agent()

        existing_history = self.user_histories.get(employee_id, [])
        user_entry = self._make_entry(
            sender="user",
            content=req.message,
            is_anonymous=getattr(req, "is_anonymous", False),
            anon_session_id=getattr(req, "anon_session_id", None),
        )
        payload_entries = [*existing_history, user_entry]
        payload_messages = self._to_langchain_messages(payload_entries)

        result = self.agent.invoke(
            {"messages": payload_messages, "user_id": employee_id},
            {"configurable": {"thread_id": employee_id}},
        )

        ai = self._extract_ai(result)
        if ai is None:
            content = getattr(result, "content", "") or FALLBACK_MESSAGE
            assistant_entry = self._make_entry(
                sender="ai",
                content=content,
                is_anonymous=user_entry["is_anonymous"],
                anon_session_id=user_entry["anon_session_id"],
            )
        else:
            assistant_entry = self._make_entry(
                sender="ai",
                content=ai.content,
                is_anonymous=user_entry["is_anonymous"],
                anon_session_id=user_entry["anon_session_id"],
            )

        self._persist_history(employee_id, user_entry)
        self._persist_history(employee_id, assistant_entry)
        return assistant_entry


well_being_agent = WellBeingAgent()
