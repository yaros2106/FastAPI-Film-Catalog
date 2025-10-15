from fastapi import APIRouter, Request, status
from starlette.responses import RedirectResponse

from dependencies.films import FilmBySlug, GetFilmStorage

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.post(
    "/",
    name="films:delete",
)
def delete_film(
    request: Request,
    film: FilmBySlug,
    storage: GetFilmStorage,
) -> RedirectResponse:
    storage.delete_by_slug(film.slug)
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
