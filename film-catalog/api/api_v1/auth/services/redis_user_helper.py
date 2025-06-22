from redis import Redis

from api.api_v1.auth.services.user_helper import AbstractUserHelper
from core import config


class RedisUserHelper(AbstractUserHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ):
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
        return self.redis.get(username)


redis_users = RedisUserHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
)
