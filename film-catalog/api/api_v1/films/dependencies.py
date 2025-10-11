from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)

from dependencies.auth import (
    UNSAFE_METHODS,
    user_basic_auth,
    validate_basic_auth,
)
from dependencies.films import GetFilmStorage
from schemas.film import Film
from services.auth import (
    redis_tokens,
)

static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your **Static API Token** from the developer portal. [Read more](#)",
    auto_error=False,
)


def prefetch_film(
    slug: str,
    storage: GetFilmStorage,
) -> Film:

    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug!r} not found",
    )


def required_api_token_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    validate_api_token(api_token=api_token)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
) -> None:

    if redis_tokens.token_exists(token=api_token.credentials):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return None

    if api_token:
        return validate_api_token(api_token=api_token)
    if credentials:
        return validate_basic_auth(credentials=credentials)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or credentials are required",
    )
