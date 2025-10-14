from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

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
def get_page_update_film(request: Request) -> HTMLResponse:
    return form_response.render(request=request)
