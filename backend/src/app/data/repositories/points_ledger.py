"""
PointsLedger repository: data access for points_ledger table.
"""
from .base import BaseRepository
from typing import Optional, List, Any


class PointsLedgerRepository(BaseRepository):
    TABLE = "points_ledger"
    ID_FIELD = "id"

    def create_entry(self, data: dict) -> int:
        return self.create(self.TABLE, data)

    def list_for_employee(self, employee_id: str) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM points_ledger WHERE employee_id = ? ORDER BY created_at DESC", (employee_id,))
        rows = cur.fetchall()
        return [dict(r) for r in rows]
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
