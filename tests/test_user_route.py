# tests/test_user_route.py
from fastapi.testclient import TestClient
from main import App
import pytest

app = App().app
client = TestClient(app)

def test_read_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == [{"username": "Rick"}, {"username": "Morty"}]

@pytest.mark.parametrize("user", [{"id": 1,"username": "TestUser", "email": "testuser@example.com"}])
def test_create_user(user):
    response = client.post("/api/v1/users/", json=user)
    assert response.status_code == 200
    assert response.json() == user
