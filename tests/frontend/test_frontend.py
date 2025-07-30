"""validate that the frontend endpoints return proper behaviors and html responses"""

import re
from fastapi.testclient import TestClient

from main import app

from test_constants import regexes

client = TestClient(app)


def test_get_homepage():
    """hit the frontpage and make sure it gives a reasonable response"""
    response = client.get("/")
    assert response.status_code == 200


def test_get_secret_value_set_from_api_context():
    """hit the get-sectet page with a valid secret set by the rest api and make
    sure it gives a good response"""
    response = client.post("api/v1/add-secret", data={"secret_value": "test-string"})
    assert response.status_code == 200
    secret_uuid = response.json()["uuid"]

    response = client.get(f"get-secret/{secret_uuid}")
    assert response.status_code == 200
    assert "test-string" in response.text


def test_get_secret_value_set_from_frontend_context():
    """hit the get-sectet page with a valid secret set by the rest api and make
    sure it gives a good response"""
    response = client.post(
        "api/v1/add-secret",
        data={"secret_value": "test-string"},
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200
    secret_uuid_matches = re.search(f"get-secret/({regexes.UUID_REGEX})", response.text)
    assert secret_uuid_matches is not None
    secret_uuid = secret_uuid_matches.group(1)

    response = client.get(f"get-secret/{secret_uuid}")
    assert response.status_code == 200
    assert "test-string" in response.text


def test_get_secret_with_no_value_set():
    """hit the get-secret page with a secret that is not populated and make
    sure it gives us a 404"""
    response = client.get("get-secret/abc123")
    assert response.status_code == 404
