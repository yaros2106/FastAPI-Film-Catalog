from fastapi import APIRouter, Request, status
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.films import FilmBySlug, GetFilmStorage
from schemas.film import FilmUpdate
from services.films import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)

form_response = FormResponseHelper(
    model=FilmUpdate,
    template_name="films/update.html",
)


@router.get(
    "/",
    name="films:update_view",
)
async def get_page_update_film(
    request: Request,
    film: FilmBySlug,
) -> HTMLResponse:
    film_update = FilmUpdate(**film.model_dump())
    return form_response.render(
        request=request,
        form_data=film_update,
        film=film,
    )


@router.post(
    "/",
    name="films:update",
    response_model=None,
)
async def update_film(
    request: Request,
    storage: GetFilmStorage,
    film: FilmBySlug,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        film_update = FilmUpdate.model_validate(form)

    storage.update(
        film=film,
        film_in=film_update,
    )
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
