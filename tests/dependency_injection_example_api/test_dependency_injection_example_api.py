"""this is an example about how to use pytest-fastapi-deps"""

from fastapi.testclient import TestClient
from main import app
from dep_injection_example.dep_injection_example import get_message_to_send  # type: ignore

client = TestClient(app)


def mock_function_to_inject(message_to_return: int) -> str:
    """use this fucntion to override the message behavior of the api to
    something we can lock down with our test case."""
    possible_responses = ["this was injected"]
    return possible_responses[message_to_return]


def test_dependency_injection_example(fastapi_dep):  # type: ignore
    """hit the dependency_injection_example endpoint but override it's print
    function to show how to do dependency injection"""
    with fastapi_dep(app).override(  # type: ignore
        {get_message_to_send: mock_function_to_inject}
    ):
        response = client.get(
            "api/v1/dependency-injection-example", params={"message_to_return": 0}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "this was injected"}
