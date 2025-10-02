from typing import Any

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
    response_class=HTMLResponse,
    include_in_schema=False,
)
def read_root(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )
