from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1 import mentoring


app = FastAPI()
app.include_router(mentoring.router)
client = TestClient(app)


def test_get_mentor_returns_profile() -> None:
    response = client.get("/api/v1/mentoring/mentors/EMP001")

    assert response.status_code == 200
    data = response.json()
    assert data["employeeId"] == "EMP001"
    assert data["name"]
