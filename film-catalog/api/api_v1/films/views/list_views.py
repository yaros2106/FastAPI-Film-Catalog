from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.films.crud import storage
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


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    film: FilmCreate,
) -> Film:
    return storage.create(film)
