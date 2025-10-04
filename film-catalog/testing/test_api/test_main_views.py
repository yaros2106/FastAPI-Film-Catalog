import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.templatetest


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.template.name == "home.html"  # type: ignore[attr-defined]
