"""
API: Marketplace

Purpose
- Serve items catalog and support redemption with points.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/marketplace/items
- POST /api/v1/marketplace/redeem
"""

from typing import List
from app.models.pydantic_schemas import MarketplaceItemDetail


EXPECTED_ROUTES: List[str] = [
    "/api/v1/marketplace/items",
    "/api/v1/marketplace/redeem",
]


def list_items() -> List[MarketplaceItemDetail]:
    """
    Contract: return available rewards items with stock and points.
    Returns: List[MarketplaceItemDetail]
    """
    # Placeholder
    raise NotImplementedError


def redeem(employee_id: str, item_id: str) -> MarketplaceItemDetail:
    """
    Contract: adjust points and record redemption.
    Returns: MarketplaceItemDetail
    """
    # Placeholder
    raise NotImplementedError

