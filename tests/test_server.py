import time

import pytest
import requests

from FastHTTPMock.server import MockServer


@pytest.fixture
def mock_server():
    server = MockServer()
    server.start(port=8001)
    time.sleep(1)  # Wait for server to start
    yield server
    server.stop()


def test_basic_mock_functionality(mock_server):
    # Add interaction
    interaction = {
        "request": {"method": "GET", "path": "/test"},
        "response": {"status": 200, "body": {"message": "success"}},
    }

    resp = requests.post("http://localhost:8001/mock/interaction", json=interaction)
    interaction_id = resp.json()["id"]

    # Test the mock endpoint
    resp = requests.get("http://localhost:8001/test")
    assert resp.status_code == 200
    assert resp.json() == {"message": "success"}

    # Verify calls
    resp = requests.get(f"http://localhost:8001/mock/interaction/{interaction_id}")
    assert resp.json()["call_count"] == 1


def test_check_mock_interaction_reset(mock_server):
    # Add interaction
    interaction = {
        "request": {"method": "GET", "path": "/test"},
        "response": {"status": 200, "body": {"message": "success"}},
    }

    resp = requests.post("http://localhost:8001/mock/interaction", json=interaction)
    interaction_id = resp.json()["id"]

    # Test the mock endpoint
    resp = requests.get("http://localhost:8001/test")
    assert resp.status_code == 200
    assert resp.json() == {"message": "success"}

    # Verify calls
    resp = requests.get(f"http://localhost:8001/mock/interaction/{interaction_id}")
    assert resp.json()["call_count"] == 1

    # Delete interactions calls
    resp = requests.delete("http://localhost:8001/mock/interactions")
    assert resp.status_code == 200
    assert resp.json()["interactions_count"] == 0
