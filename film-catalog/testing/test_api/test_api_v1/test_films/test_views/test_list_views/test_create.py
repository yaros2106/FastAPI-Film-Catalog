import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from starlette import status

from main import app
from schemas.film import Film, FilmCreate
from testing.conftest import build_film_create_random_slug

pytestmark = pytest.mark.apitest


def test_create_film(auth_client: TestClient) -> None:
    url = app.url_path_for("create_film")
    film_in = build_film_create_random_slug()
    data: dict[str, str] = film_in.model_dump()
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = FilmCreate(**response_data)
    assert received_values == film_in, response_data


def test_create_movie_already_exists(
    film: Film,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("create_film")
    film_in = FilmCreate(**film.model_dump())
    data: dict[str, str] = film_in.model_dump()
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Film with slug='{film_in.slug}' already exists"
    assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalidFilm:
    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too short slug"),
            pytest.param(("a" * 51, "string_too_long"), id="too long slug"),
        ],
    )
    def film_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, str], str]:
        slug, expected_error = request.param
        film_in = build_film_create_random_slug()
        data: dict[str, str] = film_in.model_dump()
        data["slug"] = slug
        return data, expected_error

    def test_invalid_slug(
        self,
        film_create_values: tuple[dict[str, str], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_film")
        film_in, expected_error = film_create_values
        response = auth_client.post(url=url, json=film_in)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_error, response.text
