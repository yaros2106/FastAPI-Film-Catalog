import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.films.crud import storage
from schemas.film import Film, FilmCreate

if getenv("TESTING") != "1":
    pytest.exit("Environment is not ready for testing")


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


@pytest.fixture()
def existing_film() -> Generator[Film]:
    existing_film = create_film()
    yield existing_film
    storage.delete(existing_film)
