import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.requests import Request

from services.auth import redis_users

log = logging.getLogger(__name__)


UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)
user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Your basic username and password auth  ",
    auto_error=False,
)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
) -> None:
    log.info("user credentials: %s", credentials)
    if credentials and redis_users.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    ):
        log.info("user is authenticated: %s", credentials.username)
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return
    validate_basic_auth(credentials=credentials)
