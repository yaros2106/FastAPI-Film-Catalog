import random

from typing import Annotated

from annotated_types import (
    Len,
    Ge,
    Le,
)

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
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


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    title: Annotated[
        str,
        Len(min_length=3, max_length=25),
        Form(),
    ],
    description: Annotated[
        str,
        Len(min_length=3, max_length=100),
        Form(),
    ],
    year: Annotated[
        int,
        Ge(1900),
        Le(2050),
        Form(),
    ],
    duration_minutes: Annotated[
        int,
        Ge(5),
        Le(5000),
        Form(),
    ],
):
    return Film(
        film_id=random.randint(4, 100),
        title=title,
        description=description,
        year=year,
        duration_minutes=duration_minutes,
    )
