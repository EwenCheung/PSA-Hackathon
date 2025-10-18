"""
API v1: Marketplace Router

Purpose
- Serve items catalog and support redemption with points.

Routes:
- GET /api/v1/marketplace/items
- POST /api/v1/marketplace/redeem
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.pydantic_schemas import MarketplaceItemDetail, RedemptionRequest

# Create router
router = APIRouter(
    prefix="/api/v1/marketplace",
    tags=["Marketplace"],
)


@router.get("/items", response_model=List[MarketplaceItemDetail])
async def list_items():
    """
    Get available rewards items with stock and points.
    
    Returns:
        List[MarketplaceItemDetail]: Available marketplace items
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Marketplace listing not yet implemented"
    )


@router.post("/redeem", response_model=MarketplaceItemDetail)
async def redeem_item(request: RedemptionRequest):
    """
    Redeem an item with points.
    
    Args:
        request: Redemption request with employee_id and item_id
        
    Returns:
        MarketplaceItemDetail: The redeemed item details
        
    Raises:
        HTTPException: 501 Not Implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Redemption not yet implemented"
    )

