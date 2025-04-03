import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup?email=test@student.com")
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@student.com for Chess Club"

def test_signup_duplicate():
    client.post("/activities/Chess Club/signup?email=test@student.com")
    response = client.post("/activities/Chess Club/signup?email=test@student.com")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_unregister_from_activity():
    client.post("/activities/Chess Club/signup?email=test@student.com")
    response = client.post("/activities/Chess Club/unregister?email=test@student.com")
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered test@student.com from Chess Club"

def test_unregister_nonexistent():
    response = client.post("/activities/Chess Club/unregister?email=nonexistent@student.com")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up"