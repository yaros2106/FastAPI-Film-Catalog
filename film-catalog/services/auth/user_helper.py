from abc import ABC, abstractmethod


class AbstractUserHelper(ABC):
    """
    - получить пароль по username
    - сравнить этот пароль с паролем в БД
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        Находим пароль по переданному username.
        Возвращаем, если найден

        :param username: - имя пользователя
        :return: возвращаем пароль по пользователю, если найден
        """

    @classmethod
    def check_password_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Проверка паролей на совпадение
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверяет, валиден ли пароль
        :param username: - чей пароль проверить`
        :param password: - переданный пароль, проверить с тем, что в БД
        :return: True если совпадает, иначе False
        """

        db_password = self.get_user_password(username=username)
        if db_password is None:
            return False
        return self.check_password_match(
            password2=db_password,
            password1=password,
        )
