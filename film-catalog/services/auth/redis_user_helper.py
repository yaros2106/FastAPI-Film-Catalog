from typing import cast

from redis import Redis

from core.config import settings
from services.auth.user_helper import AbstractUserHelper


class RedisUserHelper(AbstractUserHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        return cast(
            str | None,
            self.redis.get(username),
        )


redis_users = RedisUserHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.users,
)
