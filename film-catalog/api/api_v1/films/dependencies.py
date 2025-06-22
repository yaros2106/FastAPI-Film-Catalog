import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    status,
    Depends,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from api.api_v1.films.crud import storage
from schemas.film import Film
from api.api_v1.auth.services import (
    redis_tokens,
    redis_users,
)

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your **Static API Token** from the developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Your basic username and password auth  ",
    auto_error=False,
)


def prefetch_film(
    slug: str,
) -> Film:

    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug!r} not found",
    )


def background_save_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    # сначала выполняется код до входа в view
    yield
    # код после выхода из view
    if request.method in UNSAFE_METHODS:
        log.info("added background task for saving state")
        background_tasks.add_task(storage.save_state)


def required_api_token_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
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
):

    if redis_tokens.token_exists(token=api_token.credentials):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return
    validate_basic_auth(credentials=credentials)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    log.info("user credentials: %s", credentials)
    if credentials and redis_users.validate_user_password(
        credentials.username,
        credentials.password,
    ):
        log.info("user is authenticated: %s", credentials.username)
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
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
):
    if request.method not in UNSAFE_METHODS:
        return

    if api_token:
        return validate_api_token(api_token=api_token)
    if credentials:
        return validate_basic_auth(credentials=credentials)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or credentials are required",
    )
