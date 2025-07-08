import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.films.crud import storage
from schemas.film import (
    Film,
    FilmCreate,
    FilmPartialUpdate,
    FilmUpdate,
)

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    raise OSError(msg)


class FilmsStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = self.create_film()

    def tearDown(self) -> None:
        storage.delete(self.film)

    def create_film(self) -> Film:
        film = FilmCreate(
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
        return storage.create(film)

    def test_update(self) -> None:
        film_update = FilmUpdate(
            **self.film.model_dump(),
        )
        film_update.title = "updated title"
        source_title = self.film.title
        updated_film = storage.update(
            film=self.film,
            film_in=film_update,
        )
        self.assertNotEqual(
            source_title,
            updated_film.title,
        )
        self.assertEqual(
            film_update,
            FilmUpdate(**updated_film.model_dump()),
        )

    def test_update_partial(self) -> None:
        film_partial_update = FilmPartialUpdate(
            title="updated title",
        )
        source_title = self.film.title
        updated_partial_film = storage.update_partial(
            film=self.film,
            film_in=film_partial_update,
        )
        self.assertNotEqual(
            source_title,
            updated_partial_film.title,
        )
        self.assertEqual(
            film_partial_update.title,
            updated_partial_film.title,
        )
