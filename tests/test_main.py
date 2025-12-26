import pytest
from fastapi.testclient import TestClient
from app.main import app

# Sets up the client for every test
@pytest.fixture
def client():
    return TestClient(app)

# Smoke Test
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "version": "1.0.0"}

# Parametrized Test
@pytest.mark.parametrize("input_text, expected_count, expected_question", [
    ("Hello world", 2, False),
    ("Is this a test?", 4, True),
    ("AI automation is the future", 5, False),
])
def test_analyze_text_logic(client, input_text, expected_count, expected_question):
    payload = {"text": input_text}
    response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == expected_count
    assert data["is_question"] == expected_question

# Error Handling Test
def test_analyze_empty_text(client):
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text cannot be empty"