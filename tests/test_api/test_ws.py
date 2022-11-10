from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

import pytest

from main import app

@pytest.mark.api
def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.api
def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws/connect/1") as websocket:
        data = websocket.receive_json()
        assert data == {"Connected to socket: ":1}