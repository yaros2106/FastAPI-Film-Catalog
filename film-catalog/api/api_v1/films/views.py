from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
)

from api.api_v1.films.crud import FILM_LIST
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film


router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get(
    "/",
    response_model=list[Film],
)
def get_films():
    return FILM_LIST


@router.get(
    "/{film_id}",
    response_model=Film,
)
def get_film_by_id(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> Film:
    return film
