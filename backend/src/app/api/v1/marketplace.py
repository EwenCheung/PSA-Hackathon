"""
API: Marketplace

Purpose
- Serve items catalog and support redemption with points.

Routes (contracts only; implemented later via FastAPI):
- GET /api/v1/marketplace/items
- POST /api/v1/marketplace/redeem
"""
from typing import Dict, List


EXPECTED_ROUTES: List[str] = [
    "/api/v1/marketplace/items",
    "/api/v1/marketplace/redeem",
]


def list_items() -> List[Dict]:
    """Contract: return available rewards items with stock and points."""
    raise NotImplementedError


def redeem(employee_id: str, item_id: str) -> Dict:
    """Contract: adjust points and record redemption."""
    raise NotImplementedError

