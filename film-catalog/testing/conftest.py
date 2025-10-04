import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from schemas.film import Film, FilmCreate
from storage.films.crud import storage


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit("Environment is not ready for testing")


def build_film_create(
    slug: str,
    description: str = "some description",
    title: str = "some title",
) -> FilmCreate:
    return FilmCreate(
        slug=slug,
        title=title,
        description=description,
        year=2000,
        duration_minutes=100,
    )


def build_film_create_random_slug(
    description: str = "some description",
    title: str = "some title",
) -> FilmCreate:
    return build_film_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description=description,
        title=title,
    )


def create_film(
    slug: str,
    description: str = "some description",
    title: str = "some title",
) -> Film:
    film = build_film_create(
        slug=slug,
        description=description,
        title=title,
    )
    return storage.create(film)


def create_film_random_slug(
    description: str = "some description",
    title: str = "some title",
) -> Film:
    film = build_film_create_random_slug(
        description=description,
        title=title,
    )
    return storage.create(film)


@pytest.fixture()
def film() -> Generator[Film]:
    existing_film = create_film_random_slug()
    yield existing_film
    storage.delete(existing_film)
