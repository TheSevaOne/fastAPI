from app.main import start
from fastapi.testclient import TestClient
import pytest
import random
import string
import asyncpg


async def clear(column, data):
    conn = await asyncpg.connect(user='admin', password='admin', database='test', host="localhost", port="5444")
    result = await conn.execute('delete from users where $1=$2', str(column), str(data))
    await conn.close()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


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
    response = client.get("/logout")
    assert response.status_code == 200


def test_login_ok(client):
    client.post(
        "/login", data={"username": "admin", "password": "admin"})
    response = client.get("/logout")
    assert response.status_code == 200


def test_register(client):
    username = get_random_string(7)
    password = get_random_string(10)
    client.post("/register", data={"username": username, "password": password})
    response = client.post("/login", data={"username": username, "password": password})  
    clear('username', username)
    assert response.status_code == 200
