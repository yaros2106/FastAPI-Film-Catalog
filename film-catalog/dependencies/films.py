from typing import Annotated

from fastapi import Depends, HTTPException, Request
from starlette import status

from schemas.film import Film
from storage.films import FilmsStorage


def get_films_storage(
    request: Request,
) -> FilmsStorage:
    return request.app.state.films_storage  # type: ignore[no-any-return]


GetFilmStorage = Annotated[
    FilmsStorage,
    Depends(get_films_storage),
]


def prefetch_film(
    slug: str,
    storage: GetFilmStorage,
) -> Film:

    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug!r} not found",
    )


FilmBySlug = Annotated[
    Film,
    Depends(prefetch_film),
]
