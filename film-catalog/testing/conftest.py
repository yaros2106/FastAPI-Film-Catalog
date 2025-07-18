import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.films.crud import storage
from schemas.film import Film, FilmCreate

if getenv("TESTING") != "1":
    pytest.exit("Environment is not ready for testing")


def build_film_create(slug: str) -> FilmCreate:
    return FilmCreate(
        slug=slug,
        title="title",
        description="description",
        year=2000,
        duration_minutes=100,
    )


def build_film_create_random_slug() -> FilmCreate:
    return build_film_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
    )


def create_film(slug: str) -> Film:
    film = build_film_create(slug)
    return storage.create(film)


def create_film_random_slug() -> Film:
    film = build_film_create_random_slug()
    return storage.create(film)


@pytest.fixture()
def film() -> Generator[Film]:
    existing_film = create_film_random_slug()
    yield existing_film
    storage.delete(existing_film)
