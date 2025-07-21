import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.films.crud import storage
from main import app
from schemas.film import Film
from testing.conftest import create_film


@pytest.fixture(
    params=[
        pytest.param("some-slug", id="normal slug"),
        pytest.param("slug", id="short slug"),
        pytest.param("abc", id="min slug"),
        pytest.param("a" * 50, id="max slug"),
    ],
)
def film(request: SubRequest) -> Film:
    return create_film(request.param)


@pytest.mark.apitest
def test_delete_film(
    film: Film,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("delete_film", slug=film.slug)
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(film.slug), response.text
