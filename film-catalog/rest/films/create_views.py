from fastapi import APIRouter, Request, status
from pydantic import ValidationError
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.films import GetFilmStorage
from schemas.film import FilmCreate
from services.films import FormResponseHelper
from storage.films.exceptions import FilmAlreadyExistsError

router = APIRouter(
    prefix="/create",
)


form_response = FormResponseHelper(
    model=FilmCreate,
    template_name="films/create.html",
)


@router.get(
    "/",
    name="films:create_view",
)
def get_page_create_film(request: Request) -> HTMLResponse:
    return form_response.render(request=request)


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
            return form_response.render(
                request,
                form_data=form,
                pydantic_error=e,
                validated=True,
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
    return form_response.render(
        request,
        errors=errors,
        form_data=film_create,
        validated=True,
    )
