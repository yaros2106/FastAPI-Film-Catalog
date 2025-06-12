import logging

from fastapi import (
    FastAPI,
    Request,
)

from api import router as api_router
from core import config


logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

app = FastAPI(
    title="Film Catalog",
)

app.include_router(api_router)


@app.get(
    "/",
    tags=["Docs"],
)
def read_root(
    request: Request,
):

    docs_url = request.url.replace(
        path="/docs",
    )

    return {
        "docs": str(docs_url),
    }
