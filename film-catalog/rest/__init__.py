from fastapi import APIRouter

from rest.films import router as films_views_router
from rest.main_views import router as main_view_router

router = APIRouter(
    include_in_schema=False,
)
router.include_router(main_view_router)
router.include_router(films_views_router)
