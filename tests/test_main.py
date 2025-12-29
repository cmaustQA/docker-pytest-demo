import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

# Parametrized Testing (Data-Driven)
@pytest.mark.parametrize("username, fake_repos, fake_followers, expected_grade", [
    ("newbie_dev", 2, 1, "Junior"),       # Case 1: Junior
    ("mid_level", 20, 10, "Senior"),      # Case 2: Senior
    ("rockstar_dev", 100, 500, "Rockstar"), # Case 3: Rockstar
    ("edge_case", 11, 6, "Senior"),       # Case 4: Boundary value
])
@respx.mock
def test_user_grading_logic(client, username, fake_repos, fake_followers, expected_grade):
    # 1. ARRANGE
    # Dynamically mock the user based on the inputs above
    respx.get(f"https://api.github.com/users/{username}").mock(
        return_value=Response(200, json={
            "public_repos": fake_repos, 
            "followers": fake_followers
        })
    )

    # 2. ACT
    response = client.post("/analyze_user", json={"username": username})

    # 3. ASSERT
    assert response.status_code == 200
    assert response.json()["assessed_grade"] == expected_grade