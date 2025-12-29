import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

# SCENARIO 1: The Happy Path (Mocking a Rockstar User)
@respx.mock
def test_analyze_rockstar_user(client):
    # ARRANGE: "Intercept" the call to GitHub
    # We force it to return specific data, so our test is deterministic.
    respx.get("https://api.github.com/users/octocat").mock(
        return_value=Response(200, json={
            "public_repos": 60, 
            "followers": 100, 
            "id": 123
        })
    )

    # ACT: Call our API
    response = client.post("/analyze_user", json={"username": "octocat"})

    # ASSERT: Check our logic
    assert response.status_code == 200
    data = response.json()
    assert data["assessed_grade"] == "Rockstar" 
    assert data["stats"]["repos"] == 60

# SCENARIO 2: The Error Path (Mocking GitHub Downtime)
@respx.mock
def test_github_downtime(client):
    # ARRANGE: Simulate GitHub crashing (Returning 500)
    respx.get("https://api.github.com/users/failguy").mock(
        return_value=Response(500)
    )

    # ACT
    response = client.post("/analyze_user", json={"username": "failguy"})

    # ASSERT: Ensure our API handles it gracefully (returns 503, not crash)
    assert response.status_code == 503
    assert response.json()["detail"] == "GitHub API unavailable"

# SCENARIO 3: Validation (Pydantic Check)
def test_empty_username(client):
    response = client.post("/analyze_user", json={"username": ""})
    assert response.status_code == 400