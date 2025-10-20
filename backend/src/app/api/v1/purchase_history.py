"""
API: Purchase History

Purpose:
- Manage employee points and purchases for the marketplace.
- Data stored in 'purchase_history.json'.
"""
from pathlib import Path
import json
from typing import List, Dict
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/v1/purchase_history",
    tags=["PurchaseHistory"],
)

# Path to your JSON database
JSON_PATH = Path(__file__).resolve().parent / "purchase_history.json"

# ---------- Utility Functions ----------
def load_data() -> List[Dict]:
    if not JSON_PATH.exists():
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: List[Dict]):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def find_employee(data: List[Dict], employee_id: str) -> Dict:
    for emp in data:
        if emp.get("id") == employee_id:
            return emp
    return {}

# ---------- Routes ----------

@router.get("/")
def list_all_purchase_history():
    """Return all employee purchase histories."""
    data = load_data()
    return data

@router.get("/{employee_id}/points")
def get_employee_points(employee_id: str):
    """Get current points for a specific employee."""
    data = load_data()
    emp = find_employee(data, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"employee_id": employee_id, "points": emp.get("points", 0)}

@router.get("/{employee_id}/bought_items")
def get_employee_bought_items(employee_id: str):
    """Get bought items for a specific employee."""
    data = load_data()
    emp = find_employee(data, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"employee_id": employee_id, "bought_items": emp.get("bought_items", [])}

@router.post("/{employee_id}/use_points")
def use_points(employee_id: str, points: int):
    """Deduct points from an employee."""
    data = load_data()
    emp = find_employee(data, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    current_points = emp.get("points", 0)
    if points > current_points:
        raise HTTPException(status_code=400, detail="Not enough points")
    
    emp["points"] = current_points - points
    save_data(data)
    return {"employee_id": employee_id, "points_remaining": emp["points"]}

@router.post("/{employee_id}/add_item")
def add_item(employee_id: str, item_name: str, cost: int):
    """
    Add a purchased item and deduct points.
    Returns error if insufficient points.
    """
    data = load_data()
    emp = find_employee(data, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    current_points = emp.get("points", 0)
    if cost > current_points:
        raise HTTPException(status_code=400, detail="Not enough points to purchase this item")

    emp["points"] = current_points - cost
    emp.setdefault("bought_items", []).append(item_name)
    save_data(data)

    return {
        "employee_id": employee_id,
        "item_added": item_name,
        "points_remaining": emp["points"],
        "bought_items": emp["bought_items"]
    }
