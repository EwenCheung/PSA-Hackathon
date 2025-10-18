"""
WellbeingService: Business logic for wellbeing domain.
"""
from app.data.repositories.wellbeing_message import WellbeingMessageRepository
from app.data.repositories.sentiment_message import SentimentMessageRepository
from app.data.repositories.sentiment_snapshot import SentimentSnapshotRepository
from app.models.pydantic_schemas import WellbeingMessageDetail, SentimentSnapshotDetail
from app.core.db import get_connection
from typing import List

class WellbeingService:
    def __init__(self):
        conn = get_connection()
        self.message_repo = WellbeingMessageRepository(conn)
        self.sentiment_repo = SentimentMessageRepository(conn)
        self.snapshot_repo = SentimentSnapshotRepository(conn)

    def get_conversation_history(self, employee_id: str, include_anon: bool = True) -> List[WellbeingMessageDetail]:
        messages = self.message_repo.list_messages()
        filtered = [WellbeingMessageDetail(**m) for m in messages if m.get("employee_id") == employee_id and (include_anon or not m.get("is_anonymous"))]
        return filtered

    def send_message(self, employee_id: str, content: str, is_anonymous: bool = False) -> WellbeingMessageDetail:
        data = {"employee_id": employee_id, "content": content, "is_anonymous": int(is_anonymous)}
        msg_id = self.message_repo.create(self.message_repo.TABLE, data)
        msg = self.message_repo.get_message(msg_id)
        return WellbeingMessageDetail(**msg)

    def analyze_sentiment(self, message_content: str) -> dict:
        # Placeholder: returns neutral sentiment
        return {"label": "neutral", "score": 0.0}

    def get_sentiment_trend(self, employee_id: str, days: int = 7) -> List[SentimentSnapshotDetail]:
        snapshots = self.snapshot_repo.list_snapshots()
        filtered = [SentimentSnapshotDetail(**s) for s in snapshots if s.get("employee_id") == employee_id]
        return filtered

    def create_daily_snapshot(self, employee_id: str, date: str) -> SentimentSnapshotDetail:
        data = {"employee_id": employee_id, "day": date, "label": "neutral", "average_score": 0.0, "messages_count": 0, "created_at": date}
        snap_id = self.snapshot_repo.create(self.snapshot_repo.TABLE, data)
        snap = self.snapshot_repo.get_snapshot(snap_id)
        return SentimentSnapshotDetail(**snap)

    def detect_wellbeing_alerts(self, threshold: float = -0.5) -> List[dict]:
        # Placeholder: no alerts
        return []
