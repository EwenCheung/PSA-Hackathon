"""Development helpers: init DB and seed sample data."""
from fastapi import APIRouter, HTTPException, status
from app.core.db import get_connection, init_db, seed_employees
import uuid
from fastapi import HTTPException, status


router = APIRouter(
    prefix="/api/v1/dev",
    tags=["Dev"],
)


@router.post("/init", status_code=status.HTTP_201_CREATED)
async def init_and_seed():
    """Initialize database schema and insert a sample employee."""
    try:
        conn = get_connection()
        init_db(conn)
        seeded_id = str(uuid.uuid4())
        sample = [
            {
                "id": seeded_id,
                "name": "Alice Example",
                "role": "engineer",
                "department_id": "eng",
                "level": "mid",
                "points_current": 120,
                "hire_date": "2024-01-15",
                "skills_map": "{}",
                "courses_enrolled_map": "{}",
                "goals_set": "[]",
            }
        ]
        seed_employees(conn, sample)
        return {"status": "ok", "seeded": 1, "employee_id": seeded_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/points_ledger/{employee_id}")
async def list_points_ledger(employee_id: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM points_ledger WHERE employee_id = ? ORDER BY created_at DESC", (employee_id,))
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
