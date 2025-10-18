"""
SentimentSnapshotRepository: Data access for sentiment_snapshots table.
"""
from .base import BaseRepository
from typing import Optional, List

class SentimentSnapshotRepository(BaseRepository):
    TABLE = "sentiment_snapshots"
    ID_FIELD = "id"

    def get_snapshot(self, snapshot_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, snapshot_id)

    def list_snapshots(self) -> List[dict]:
        return self.list_all(self.TABLE)
