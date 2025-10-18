from datetime import date, datetime

from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR
from misc.flash_messages import get_flashed_messages


def inject_current_date_and_dt(
    request: Request,  # noqa: ARG001
) -> dict[str, date]:
    today = datetime.now().date()  # noqa: DTZ005
    now = datetime.now()  # noqa: DTZ005
    return {
        "today": today,
        "now": now,
    }


def inject_features(
    request: Request,  # noqa: ARG001
) -> dict[str, list[str]]:
    features = [
        "Create films",
        "Real-time statistics",
        "Shared management",
        "Search and filter films",
        "Edit and delete existing entries",
        "Responsive design",
        "Fast server-side rendering with HTMX",
    ]
    return {
        "features": features,
    }


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[inject_current_date_and_dt, inject_features],
)
templates.env.globals[get_flashed_messages.__name__] = get_flashed_messages
