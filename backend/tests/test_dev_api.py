"""
Integration test for /api/v1/dev/init endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dev_init_endpoint():
    # Call the dev init endpoint
    response = client.post("/api/v1/dev/init")
    assert response.status_code == 201, f"Unexpected status: {response.status_code}, body: {response.text}"
    data = response.json()
    assert data["status"] == "ok"
    assert data["seeded"] == 1
    assert "employee_id" in data
    assert isinstance(data["employee_id"], str)
    assert len(data["employee_id"]) > 0


def test_points_adjust_and_ledger():
    # Initialize DB and seed
    resp = client.post("/api/v1/dev/init")
    assert resp.status_code == 201
    emp_id = resp.json()["employee_id"]

    # Adjust points by +50
    patch = client.patch(f"/api/v1/employees/{emp_id}/points?delta=50")
    assert patch.status_code == 200
    updated = patch.json()
    assert updated["id"] == emp_id
    assert updated["points_current"] >= 170  # original 120 + 50

    # Fetch ledger entries
    ledger = client.get(f"/api/v1/dev/points_ledger/{emp_id}")
    assert ledger.status_code == 200
    entries = ledger.json()
    assert len(entries) >= 1
    # top entry should have delta 50
    assert entries[0]["delta"] == 50
