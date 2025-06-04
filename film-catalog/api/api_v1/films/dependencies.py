from fastapi import HTTPException
from starlette import status

from api.api_v1.films.crud import FILM_LIST
from schemas.film import Film


def prefetch_film(
    film_id: int,
) -> Film:

    film: Film | None = next(
        (film for film in FILM_LIST if film.film_id == film_id),
        None,
    )

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with id {film_id!r} not found",
    )
