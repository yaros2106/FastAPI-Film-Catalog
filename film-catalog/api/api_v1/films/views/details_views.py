import logging
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
    FilmPartialUpdate,
    FilmRead,
)


log = logging.getLogger(__name__)

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


@router.get(
    "/",
    response_model=FilmRead,
)
def get_film_by_slug(
    film: FilmBySlug,
) -> Film:
    return film


@router.put(
    "/",
    response_model=FilmRead,
)
def update_film(
    film: FilmBySlug,
    film_in: FilmUpdate,
):
    log.info("added background task for saving state")
    return storage.update(
        film=film,
        film_in=film_in,
    )


@router.patch(
    "/",
    response_model=FilmRead,
)
def update_film_partial(
    film: FilmBySlug,
    film_in: FilmPartialUpdate,
):
    log.info("added background task for saving state")
    return storage.update_partial(
        film=film,
        film_in=film_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: FilmBySlug,
) -> None:
    storage.delete(film=film)
