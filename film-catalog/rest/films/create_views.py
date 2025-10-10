from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, ValidationError
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.films import GetFilmStorage
from schemas.film import FilmCreate
from storage.films.exceptions import FilmAlreadyExistsError
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


def create_view_validation_response(
    request: Request,
    errors: dict[str, str] | None = None,
    form_data: BaseModel | Mapping[str, Any] | None = None,
    validated: bool = True,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = FilmCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        validated=validated,
        form_data=form_data,
    )
    return templates.TemplateResponse(
        request=request,
        name="films/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@router.post(
    "/",
    name="films:create",
    response_model=None,
)
async def create_film(
    request: Request,
    storage: GetFilmStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            film_create = FilmCreate.model_validate(form)
        except ValidationError as e:
            errors: dict[str, str] = {
                str(error["loc"][0]): error["msg"] for error in e.errors()
            }
            return create_view_validation_response(
                request=request,
                errors=errors,
                form_data=form,
            )
    try:
        storage.create_or_raise_if_exists(film_create)
    except FilmAlreadyExistsError:
        errors = {
            "slug": f"film with slug {film_create.slug!r} already exists.",
        }
    else:
        return RedirectResponse(
            url=request.url_for("films:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return create_view_validation_response(
        request=request,
        errors=errors,
        form_data=film_create,
    )
