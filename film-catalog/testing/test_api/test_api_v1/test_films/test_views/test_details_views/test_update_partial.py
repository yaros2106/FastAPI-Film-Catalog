from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.film import Film
from storage.films.crud import storage
from testing.conftest import create_film_random_slug


@pytest.mark.apitest
class TestUpdatePartial:
    DESCRIPTION_MAX_LENGTH = 150
    DESCRIPTION_MIN_LENGTH = 3

    @pytest.fixture
    def film(self, request: SubRequest) -> Generator[Film]:
        description = request.param
        film = create_film_random_slug(
            description=description,
        )
        yield film
        storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description",
        [
            pytest.param(
                "some-description",
                "a" * DESCRIPTION_MIN_LENGTH,
                id="some-description-to-min-description",
            ),
            pytest.param(
                "a" * DESCRIPTION_MIN_LENGTH,
                "some-description",
                id="min-description-to-some-description",
            ),
            pytest.param(
                "a" * DESCRIPTION_MAX_LENGTH,
                "b" * DESCRIPTION_MIN_LENGTH,
                id="max-description-to-min-description",
            ),
            pytest.param(
                "c" * DESCRIPTION_MIN_LENGTH,
                "d" * DESCRIPTION_MAX_LENGTH,
                id="min-description-to-max-description",
            ),
        ],
        indirect=["film"],
    )
    def test_update_film_details_partial(
        self,
        film: Film,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_film_partial",
            slug=film.slug,
        )
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = storage.get_by_slug(film.slug)
        assert film_db
        assert film_db.description == new_description, response.text
