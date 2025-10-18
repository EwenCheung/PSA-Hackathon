"""
SentimentMessageRepository: Data access for sentiment_messages table.
"""
from .base import BaseRepository
from typing import Optional, List

class SentimentMessageRepository(BaseRepository):
    TABLE = "sentiment_messages"
    ID_FIELD = "id"

    def get_sentiment(self, sentiment_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, sentiment_id)

    def list_sentiments(self) -> List[dict]:
        return self.list_all(self.TABLE)
