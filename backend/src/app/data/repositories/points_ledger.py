"""
PointsLedgerRepository: Data access for points_ledger table.
"""
from .base import BaseRepository
from typing import Optional, List

class PointsLedgerRepository(BaseRepository):
    TABLE = "points_ledger"
    ID_FIELD = "id"

    def get_entry(self, entry_id: int) -> Optional[dict]:
        return self.get_by_id(self.TABLE, self.ID_FIELD, entry_id)

    def list_entries(self) -> List[dict]:
        return self.list_all(self.TABLE)
