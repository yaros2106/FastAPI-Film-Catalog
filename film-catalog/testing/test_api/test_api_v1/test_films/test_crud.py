import random
import string
from os import getenv
from typing import ClassVar
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


def create_film() -> Film:
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


class FilmsStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = create_film()

    def tearDown(self) -> None:
        storage.delete(self.film)

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


class FilmsStorageGetFilmTestCase(TestCase):
    FILMS_COUNT = 3
    films: ClassVar[list[Film]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.films = [create_film() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for film in cls.films:
            storage.delete(film)

    def test_get_list(self) -> None:
        db_films = storage.get()
        expected_slugs = {film.slug for film in self.films}  # {a, b, c}
        slugs = {film.slug for film in db_films}  # {a, b, c, d, e}
        expected_diff: set[str] = set()
        diff = expected_slugs - slugs  # {} если полученные есть в ожидаемых
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(
                slug=film.slug,
                msg=f"checking {film.slug}",
            ):
                db_film = storage.get_by_slug(film.slug)
                self.assertEqual(
                    film,
                    db_film,
                )
