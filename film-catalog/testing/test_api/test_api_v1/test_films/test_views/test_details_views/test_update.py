from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.films.crud import storage
from main import app
from schemas.film import Film, FilmUpdate
from testing.conftest import create_film_random_slug


class TestUpdate:
    DESCRIPTION_MAX_LENGTH = 150
    DESCRIPTION_MIN_LENGTH = 3
    TITLE_MAX_LENGTH = 3
    TITLE_MIN_LENGTH = 25

    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[Film]:
        description, title = request.param
        film = create_film_random_slug(
            description=description,
            title=title,
        )
        yield film
        storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description, new_title",
        [
            pytest.param(
                ("some description", "some title"),
                "new description",
                "new title",
                id="new-description-and-new-title",
            ),
            pytest.param(
                ("the description", "the title"),
                "some description",
                "new title",
                id="same-description-and-new-title",
            ),
            pytest.param(
                ("old description", "old title"),
                "d" * DESCRIPTION_MAX_LENGTH,
                "t" * TITLE_MAX_LENGTH,
                id="max-description-and-max-title",
            ),
            pytest.param(
                ("foo description", "bar title"),
                "a" * DESCRIPTION_MIN_LENGTH,
                "b" * TITLE_MIN_LENGTH,
                id="min-description-and-min-title",
            ),
            pytest.param(
                ("abc description", "qwe title"),
                "q" * DESCRIPTION_MIN_LENGTH,
                "qwe title",
                id="min-description-and-same-title",
            ),
        ],
        indirect=["film"],
    )
    def test_update_film_details(
        self,
        film: Film,
        new_title: str,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        film_in = FilmUpdate(
            title=new_title,
            description=new_description,
            year=2000,
            duration_minutes=555,
        )
        data = film_in.model_dump()
        url = app.url_path_for(
            "update_film",
            slug=film.slug,
        )
        response = auth_client.put(
            url,
            json=data,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = storage.get_by_slug(film.slug)
        assert film_db
        new_data = FilmUpdate(**film_db.model_dump())
        assert new_data == film_in, response.text
