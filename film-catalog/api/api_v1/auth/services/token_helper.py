import secrets
from abc import ABC, abstractmethod


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

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Get all existing tokens
        :return:
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Delete token from storage
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
