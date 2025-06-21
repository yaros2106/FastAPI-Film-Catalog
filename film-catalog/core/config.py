import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
FILM_STORAGE_FILEPATH = BASE_DIR / "films-storage.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS: frozenset[str] = frozenset(
    {
        "DJACoso2C9ugXuqDRbKvcA",
        "7vb-XqtE-sgGSsvvVbQVZA",
        "Z7xf0nvDFyG2EX11q_85Gw",
    }
)

USER_DB: dict[str, str] = {
    # username: password
    "yaros": "password",
    "sam": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
