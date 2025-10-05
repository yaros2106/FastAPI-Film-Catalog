from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from dependencies.films import GetFilmStorage
from templating import templates

router = APIRouter()

if TYPE_CHECKING:
    from schemas.film import Film


@router.get(
    "/",
    name="films:list",
    response_class=HTMLResponse,
)
def list_view(
    request: Request,
    storage: GetFilmStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    films: list[Film] = storage.get()
    context.update(
        films=films,
    )
    return templates.TemplateResponse(
        request=request,
        name="films/list.html",
        context=context,
    )
