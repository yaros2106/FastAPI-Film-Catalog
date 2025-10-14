from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from dependencies.films import FilmBySlug
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
