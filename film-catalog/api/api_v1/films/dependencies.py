from fastapi import HTTPException
from starlette import status

from api.api_v1.films.crud import storage
from schemas.film import Film


def prefetch_film(
    slug: str,
) -> Film:

    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug!r} not found",
    )
