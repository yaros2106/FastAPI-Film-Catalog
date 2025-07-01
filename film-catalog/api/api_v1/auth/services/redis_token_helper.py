from redis import Redis

from api.api_v1.auth.services.token_helper import AbstractTokenHelper
from core import config
from core.config import REDIS_TOKENS_SET_NAME


class RedisTokenHelper(AbstractTokenHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        token_set_name: str,
    ):
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.token_set_name = token_set_name

    def token_exists(self, token: str) -> bool:
        return bool(
            self.redis.sismember(
                self.token_set_name,
                token,
            )
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(self.token_set_name, token)

    def get_tokens(self) -> list[str]:
        return list(self.redis.smembers(self.token_set_name))

    def delete_token(self, token: str) -> None:
        if self.token_exists(token):
            self.redis.srem(self.token_set_name, token)


redis_tokens = RedisTokenHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    token_set_name=REDIS_TOKENS_SET_NAME,
)
