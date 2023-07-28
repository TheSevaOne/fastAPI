from app.main import start
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    with TestClient(start()) as c:
        yield c

def test_loading(client):
    response = client.get("/")
    assert response.status_code == 200


def test_auth_not(client):
    response = client.get("/user")
    assert response.status_code == 401


def test_login_fail(client):
    response = client.post(
        "/login", data={"username": "admin", "password": "0"})
    assert response.status_code == 401


def test_login_ok(client):
    client.post(
        "/login", data={"username": "admin", "password": "admin"})
    response=client.get("/logout")
    assert response.status_code==200


