"""make sure the health api endpoint works"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_check_service_health():
    """hit the v1 health endpoint and make sure it gives a good response"""
    response = client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy!"}
