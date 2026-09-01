import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities
from fastapi.testclient import TestClient

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.delete("/activities/Chess Club/unregister?email=daniel@mergington.edu")

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
