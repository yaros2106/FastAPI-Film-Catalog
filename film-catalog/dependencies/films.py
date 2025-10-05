from typing import Annotated

from fastapi import Depends, Request

from storage.films import FilmsStorage


def get_films_storage(
    request: Request,
) -> FilmsStorage:
    return request.app.state.films_storage  # type: ignore[no-any-return]


GetFilmStorage = Annotated[
    FilmsStorage,
    Depends(get_films_storage),
]
