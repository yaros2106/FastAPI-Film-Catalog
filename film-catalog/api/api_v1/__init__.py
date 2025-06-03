from fastapi import APIRouter

from .films.views import router as film_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(film_router)
