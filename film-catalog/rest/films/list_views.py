from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Form, Request
from starlette.responses import HTMLResponse

from dependencies.films import GetFilmStorage
from services.films import FormResponseHelper
from templating import templates

router = APIRouter()

if TYPE_CHECKING:
    from schemas.film import Film


form_response = FormResponseHelper(
    model=None,
    template_name="films/list.html",
)


@router.get(
    "/",
    name="films:list",
    response_class=HTMLResponse,
)
def list_view(
    request: Request,
    storage: GetFilmStorage,
) -> HTMLResponse:
    films: list[Film] = storage.get()
    return form_response.render(
        request=request,
        films=films,
    )


@router.post(
    "/",
    name="films:search",
    response_class=HTMLResponse,
)
def search_film(
    request: Request,
    storage: GetFilmStorage,
    query: Annotated[str, Form()],
) -> HTMLResponse:
    context: dict[str, Any] = {}
    films: list[Film] = storage.get()
    query_lower = query.lower()
    films = [
        f
        for f in films
        if query_lower in f.title.lower()
        or query_lower in f.description.lower()
        or query_lower in f.slug.lower()
    ]
    context.update(
        films=films,
    )
    return templates.TemplateResponse(
        request=request,
        name="films/components/films_table.html",
        context=context,
    )
