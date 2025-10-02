from datetime import UTC, date, datetime

from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR


def inject_current_date_and_dt(
    request: Request,  # noqa: ARG001
) -> dict[str, date]:
    today = datetime.now(UTC).date()
    now = datetime.now(UTC)
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
    ]
    return {
        "features": features,
    }


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[inject_current_date_and_dt, inject_features],
)
