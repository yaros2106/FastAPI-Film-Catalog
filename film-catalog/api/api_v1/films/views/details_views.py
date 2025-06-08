from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import (
    Film,
    FilmUpdate,
)

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film with slug 'some-slug' not found",
                    },
                },
            },
        },
    },
)

FilmBySlug = Annotated[
    Film,
    Depends(prefetch_film),
]


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: FilmBySlug,
) -> None:
    storage.delete(film=film)


@router.put(
    "/",
    response_model=Film,
)
def update_film(
    film: FilmBySlug,
    film_in: FilmUpdate,
):
    return storage.update(
        film=film,
        film_in=film_in,
    )


@router.get(
    "/",
    response_model=Film,
)
def get_film_by_slug(
    film: FilmBySlug,
) -> Film:
    return film
