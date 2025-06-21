import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
FILM_STORAGE_FILEPATH = BASE_DIR / "films-storage.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


USER_DB: dict[str, str] = {
    # username: password
    "yaros": "password",
    "sam": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1

REDIS_TOKENS_SET_NAME = "tokens"
