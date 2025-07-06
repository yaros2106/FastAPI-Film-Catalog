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

    def test_film_created_accepts_various_data(self) -> None:
        slug_display_limit = 10
        data: list[dict[str, str | int]] = [
            {
                "slug": "some-slug",
                "title": "some-title",
                "description": "some-description",
                "year": 2020,
                "duration_minutes": 100,
            },
            {
                # min limit value
                "slug": "slu",
                "title": "tit",
                "description": "des",
                "year": 1900,
                "duration_minutes": 5,
            },
            {
                # max limit value
                "slug": "s" * 50,
                "title": "t" * 25,
                "description": "d" * 150,
                "year": 2050,
                "duration_minutes": 5000,
            },
        ]

        for item in data:
            slug_value = str(item["slug"])
            slug_short = (
                slug_value[:slug_display_limit] + "..."
                if len(slug_value) > slug_display_limit
                else slug_value
            )
            with self.subTest(
                slug=slug_short,
                msg=f"test film: {slug_short}",
            ):
                film = FilmCreate(**item)
                self.assertEqual(item["slug"], film.slug)
                self.assertEqual(item["title"], film.title)
                self.assertEqual(item["description"], film.description)
                self.assertEqual(item["year"], film.year)
                self.assertEqual(item["duration_minutes"], film.duration_minutes)


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
            description="must_be_replaced_description",
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
