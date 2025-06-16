import logging

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import background_save_state
from schemas.film import (
    Film,
    FilmCreate,
    FilmRead,
)


log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/films", tags=["Films"], dependencies=[Depends(background_save_state)]
)


@router.get(
    "/",
    response_model=list[FilmRead],
)
def get_films() -> list[Film]:
    return storage.get()


@router.post(
    "/",
    response_model=FilmRead,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    film: FilmCreate,
) -> Film:
    return storage.create(film)
