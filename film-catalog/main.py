from fastapi import (
    FastAPI,
    Request,
)


app = FastAPI(
    title="Film Catalog",
)


@app.get("/")
def read_root(
    request: Request,
):

    docs_url = request.url.replace(
        path="/docs",
    )

    return {
        "docs": str(docs_url),
    }
