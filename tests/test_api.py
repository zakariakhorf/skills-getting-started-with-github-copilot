import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Spot check a known activity
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Basketball Club"
    email = "test_student@mergington.edu"

    # Ensure a clean state for the test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message") == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message") == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_participant():
    activity = "Science Club"
    email = "nonexistent@mergington.edu"

    # Ensure email not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
