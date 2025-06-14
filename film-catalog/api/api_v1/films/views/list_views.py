import logging

from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)

from api.api_v1.films.crud import storage
from schemas.film import (
    Film,
    FilmCreate,
    FilmRead,
)


log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
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
    background_tasks: BackgroundTasks,
) -> Film:
    background_tasks.add_task(storage.save_state)
    log.info("added background task for saving state")
    return storage.create(film)
