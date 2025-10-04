from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter(
    tags=["Docs"],
)


@router.get(
    "/",
    name="home",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def home_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )


@router.get(
    "/about/",
    name="about",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def about_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )
