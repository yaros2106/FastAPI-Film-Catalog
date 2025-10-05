from typing import Annotated

from fastapi import Depends

from core.config import settings
from storage.films import FilmsStorage


def get_films_storage() -> FilmsStorage:
    return FilmsStorage(
        hash_name=settings.redis.collection_name.films_hash,
    )


GetFilmStorage = Annotated[
    FilmsStorage,
    Depends(get_films_storage),
]
