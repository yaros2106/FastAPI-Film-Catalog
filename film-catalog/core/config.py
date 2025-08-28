import logging
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDataBaseConfig(BaseModel):
    common: int = 0
    tokens: int = 1
    users: int = 2
    films: int = 3

    @model_validator(mode="after")
    def check_unique_numbers_db(self) -> Self:
        db_numbers = list(self.model_dump().values())
        if len(set(db_numbers)) != len(db_numbers):
            msg = "Database numbers must be unique"
            raise ValueError(msg)
        return self


class RedisCollectionsNamesConfig(BaseModel):
    tokens_set: str = "tokens"
    films_hash: str = "films"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDataBaseConfig = RedisDataBaseConfig()
    collection_name: RedisCollectionsNamesConfig = RedisCollectionsNamesConfig()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",  # перезапишет файл выше, но оставит неизмененные поля
        ),
        env_prefix="FILM_CATALOG__",
        env_nested_delimiter="__",
        yaml_file=(
            BASE_DIR / "config.default.yaml",
            BASE_DIR / "config.local.yaml",
        ),
        yaml_config_section="film-catalog",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
        A tuple containing the sources and their order for loading the settings values.
        """
        return (
            init_settings,  # дефолты имеют самый низкий приоритет
            env_settings,  # переменные окружения переопределяют все кроме init_settings
            dotenv_settings,  # .env переопределяет все кроме того что выше
            file_secret_settings,  # временно не используем
            YamlConfigSettingsSource(settings_cls),  # все кроме того, что выше
        )

    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()
