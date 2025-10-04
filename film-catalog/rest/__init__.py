from fastapi import APIRouter

from .main_views import router as main_view_router

router = APIRouter(
    include_in_schema=False,
)
router.include_router(main_view_router)
