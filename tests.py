from app.main import start
from fastapi.testclient import TestClient
client=TestClient(start())
def test_loading():
  response=  client.get("/")
  assert response.status_code==200
def test_auth_not():
  response=  client.get("/user")
  assert response.status_code==401

