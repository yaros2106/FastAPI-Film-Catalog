from typing import Annotated, Any

from fastapi import APIRouter, Form, Request
from starlette.responses import HTMLResponse

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
    required_list = model_schema.get("required", [])

    context.update(
        model_schema=model_schema,
        required_list=required_list,
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
    film_create: Annotated[
        FilmCreate,
        Form(),
    ],
) -> dict[str, str | int]:
    return film_create.model_dump(mode="json")
