from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)
from pip._internal.cli import status_codes

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film, FilmCreate

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get(
    "/",
    response_model=list[Film],
)
def get_films() -> list[Film]:
    return storage.get()


@router.get(
    "/{slug}",
    response_model=Film,
)
def get_film_by_slug(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> Film:
    return film


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    film: FilmCreate,
) -> Film:
    return storage.create(film)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_film(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> None:
    storage.delete(film=film)
