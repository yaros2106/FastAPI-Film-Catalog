from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, status
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.films import GetFilmStorage
from schemas.film import FilmCreate
from templating import templates

router = APIRouter(
    prefix="/create",
)


@router.get(
    "/",
    name="films:create_view",
)
def get_page_create_film(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = FilmCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
    )
    return templates.TemplateResponse(
        request=request,
        name="films/create.html",
        context=context,
    )


@router.post(
    "/",
    name="films:create",
)
def create_film(
    request: Request,
    storage: GetFilmStorage,
    film_create: Annotated[
        FilmCreate,
        Form(),
    ],
) -> RedirectResponse:
    storage.create_or_raise_if_exists(film_create)
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
