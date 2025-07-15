import random
import string

from fastapi.testclient import TestClient
from starlette import status

from main import app
from schemas.film import Film, FilmCreate


def test_create_film(auth_client: TestClient) -> None:
    url = app.url_path_for("create_film")
    film_in = FilmCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        title="title",
        description="description",
        year=2000,
        duration_minutes=100,
    )
    data: dict[str, str] = film_in.model_dump()
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = FilmCreate(**response_data)
    assert received_values == film_in, response_data


def test_create_movie_already_exists(
    existing_film: Film,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("create_film")
    film_in = FilmCreate(**existing_film.model_dump())
    data: dict[str, str] = film_in.model_dump()
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Film with slug='{film_in.slug}' already exists"
    assert response_data["detail"] == expected_error_detail, response_data
