from unittest import TestCase

from schemas.film import (
    Film,
    FilmCreate,
    FilmPartialUpdate,
    FilmUpdate,
)


class FilmCreateTestCase(TestCase):
    def test_film_can_be_created_from_create_schema(self) -> None:
        film_in = FilmCreate(
            slug="some-slug",
            title="some-title",
            description="some-description",
            year=2020,
            duration_minutes=555,
        )
        film = Film(**film_in.model_dump())
        self.assertEqual(film_in.slug, film.slug)
        self.assertEqual(film_in.title, film.title)
        self.assertEqual(film_in.description, film.description)
        self.assertEqual(film_in.year, film.year)
        self.assertEqual(film_in.duration_minutes, film.duration_minutes)


class FilmUpdateTestCase(TestCase):
    def test_film_can_be_updated_from_update_schema(self) -> None:
        film_in = FilmUpdate(
            title="some-title",
            description="some-description",
            year=2020,
            duration_minutes=555,
        )
        film = Film(
            slug="some-slug",
            title="must_be_replaced_title",
            description="some-must_be_replaced_description",
            year=2000,
            duration_minutes=100,
        )
        for field_name, value in film_in:
            setattr(film, field_name, value)

        self.assertEqual("some-slug", film.slug)
        self.assertEqual(film_in.title, film.title)
        self.assertEqual(film_in.description, film.description)
        self.assertEqual(film_in.year, film.year)
        self.assertEqual(film_in.duration_minutes, film.duration_minutes)


class FilmPartialUpdateTestCase(TestCase):
    def test_film_can_be_partial_updated_from_partial_update_schema(self) -> None:
        film_in = FilmPartialUpdate()
        film = Film(
            slug="some-slug",
            title="some-title",
            description="some-description",
            year=2020,
            duration_minutes=555,
        )
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)

        self.assertEqual("some-slug", film.slug)
        self.assertEqual("some-title", film.title)
        self.assertEqual("some-description", film.description)
        self.assertEqual(2020, film.year)
        self.assertEqual(555, film.duration_minutes)
