"""make sure the secrets api endpoints work"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_set_secret():
    """add a secret value and make sure the response makes sense"""
    response = client.post("api/v1/add-secret", data={"secret_value": "test-string"})
    assert response.status_code == 200
    assert "url" in response.json()
    assert "uuid" in response.json()


def test_set_and_get_secret():
    """add a secret value and then go get it"""
    response = client.post("api/v1/add-secret", data={"secret_value": "test-string"})
    assert response.status_code == 200
    get_secret_uuid = response.json()["uuid"]

    response = client.get(f"api/v1/get-secret/{get_secret_uuid}")
    assert response.status_code == 200
    assert response.json()["secret_value"] == "test-string"


def test_ensure_secret_is_only_readable_once():
    """add a secret value and then go get it, then make sure we can't read it again"""
    response = client.post("api/v1/add-secret", data={"secret_value": "test-string"})
    assert response.status_code == 200
    get_secret_uuid = response.json()["uuid"]

    response = client.get(f"api/v1/get-secret/{get_secret_uuid}")
    assert response.status_code == 200
    assert response.json()["secret_value"] == "test-string"

    response = client.get(f"api/v1/get-secret/{get_secret_uuid}")
    assert response.status_code == 404


def test_get_secret_that_doesnt_exist():
    """try to get a secret that doesn't exist"""
    response = client.get("api/v1/get-secret/abc123")
    assert response.status_code == 404
