"""
MarketplaceService: Business logic for marketplace domain.
"""
from app.data.repositories.marketplace_item import MarketplaceItemRepository
from app.data.repositories.redemption import RedemptionRepository
from app.data.repositories.points_ledger import PointsLedgerRepository
from app.models.pydantic_schemas import MarketplaceItemDetail
from app.core.db import get_connection
from typing import List

class MarketplaceService:
    def __init__(self):
        conn = get_connection()
        self.item_repo = MarketplaceItemRepository(conn)
        self.redemption_repo = RedemptionRepository(conn)
        self.ledger_repo = PointsLedgerRepository(conn)

    def get_available_items(self, category: str = None) -> List[MarketplaceItemDetail]:
        items = self.item_repo.list_items()
        if category:
            items = [i for i in items if i.get("category") == category]
        return [MarketplaceItemDetail(**i) for i in items]

    def redeem_item(self, employee_id: str, item_id: int) -> dict:
        # Placeholder: create redemption and ledger entry
        redemption_data = {"employee_id": employee_id, "item_id": item_id, "points_cost": 0, "created_at": "now"}
        self.redemption_repo.create(self.redemption_repo.TABLE, redemption_data)
        ledger_data = {"employee_id": employee_id, "delta": -10, "source": "redemption", "reference_id": str(item_id), "created_at": "now"}
        self.ledger_repo.create(self.ledger_repo.TABLE, ledger_data)
        return {"redemption": redemption_data, "ledger": ledger_data}

    def validate_sufficient_points(self, employee_id: str, cost: int) -> bool:
        # Placeholder: always true
        return True
