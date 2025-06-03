from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from schemas.film import Film

app = FastAPI(
    title="Film Catalog",
)


@app.get("/")
def read_root(
    request: Request,
):

    docs_url = request.url.replace(
        path="/docs",
    )

    return {
        "docs": str(docs_url),
    }


FILM_LIST = [
    Film(
        id=1,
        title="The Walking Dead",
        description="A group of survivors navigates a post-apocalyptic world overrun by zombies",
        year=2010,
        duration_minutes=44,
    ),
    Film(
        id=2,
        title="Outcast",
        description="After a plane crash, a FedEx executive struggles to survive on a deserted island",
        year=2000,
        duration_minutes=143,
    ),
    Film(
        id=3,
        title="The Matrix",
        description="A computer hacker learns about the true nature of his reality and his role in the war against its controllers",
        year=1999,
        duration_minutes=136,
    ),
]


@app.get(
    "/films",
    response_model=list[Film],
)
def get_films():
    return FILM_LIST


def prefetch_film(
    film_id: int,
) -> Film:

    film: Film | None = next((film for film in FILM_LIST if film.id == film_id), None)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with id {film_id!r} not found",
    )


@app.get(
    "/films/{film_id}",
    response_model=Film,
)
def get_film_by_id(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film
