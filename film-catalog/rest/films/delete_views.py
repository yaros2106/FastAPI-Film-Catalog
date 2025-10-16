from fastapi import APIRouter, Response, status

from dependencies.films import FilmBySlug, GetFilmStorage

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.delete(
    "/",
    name="films:delete",
)
def delete_film(
    film: FilmBySlug,
    storage: GetFilmStorage,
) -> Response:
    storage.delete_by_slug(film.slug)
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
