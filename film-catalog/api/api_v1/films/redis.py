import secrets
from abc import ABC, abstractmethod

from redis import Redis

from core import config
from core.config import REDIS_TOKENS_SET_NAME


class AbstractTokenHelper(ABC):
    """
    Что нужно от обертки:
    - проверить на существование токена
    - добавить токен в хранилище
    - сгенерировать новый токен и добавить в хранилище
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Check if token exists

        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Save token into storage

        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


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


redis_tokens = RedisTokenHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    token_set_name=REDIS_TOKENS_SET_NAME,
)
