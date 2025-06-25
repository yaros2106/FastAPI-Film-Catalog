import logging

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import (
    required_api_token_for_unsafe_methods,
    user_basic_auth_required_for_unsafe_methods,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.film import (
    Film,
    FilmCreate,
    FilmRead,
)


log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[
        # Depends(required_api_token_for_unsafe_methods),
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid username or password",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=list[FilmRead],
)
def get_films() -> list[Film]:
    return storage.get()


@router.post(
    "/",
    response_model=FilmRead,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    film: FilmCreate,
) -> Film:
    return storage.create(film)
