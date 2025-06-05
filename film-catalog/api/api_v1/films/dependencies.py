from fastapi import HTTPException
from starlette import status

from api.api_v1.films.crud import FILM_LIST
from schemas.film import Film


def prefetch_film(
    slug: str,
) -> Film:

    film: Film | None = next(
        (film for film in FILM_LIST if film.slug == slug),
        None,
    )

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug!r} not found",
    )
