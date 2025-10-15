from fastapi import APIRouter, Request, status
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.post(
    "/",
    name="films:delete",
)
def delete_film(
    request: Request,
) -> RedirectResponse:
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
