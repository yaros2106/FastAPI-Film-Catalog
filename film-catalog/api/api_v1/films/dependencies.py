import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
)
from starlette import status

from api.api_v1.films.crud import storage
from schemas.film import Film


log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


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


def background_save_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    # сначала выполняется код до входа в view
    yield
    # код после выхода из view
    if request.method in UNSAFE_METHODS:
        log.info("added background task for saving state")
        background_tasks.add_task(storage.save_state)
