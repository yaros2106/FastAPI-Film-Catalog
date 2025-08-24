__all__ = (
    "FilmAlreadyExistsError",
    "storage",
)

import logging

from pydantic import (
    BaseModel,
)
from redis import Redis

from core import config
from core.config import settings
from schemas.film import (
    Film,
    FilmCreate,
    FilmPartialUpdate,
    FilmUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmBaseError(Exception):
    """
    Base exception class for film related errors.
    """


class FilmAlreadyExistsError(FilmBaseError):
    """
    Raised when a film on creation already exists.
    """


class FilmsStorage(BaseModel):

    def save_film_data(self, film: Film) -> None:
        redis.hset(
            name=config.REDIS_FILMS_HASH_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )

    def get(self) -> list[Film]:
        data = redis.hvals(name=config.REDIS_FILMS_HASH_NAME)
        return [Film.model_validate_json(film) for film in data]

    def get_by_slug(self, slug: str) -> Film | None:
        data = redis.hget(
            name=config.REDIS_FILMS_HASH_NAME,
            key=slug,
        )
        if data:
            return Film.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=config.REDIS_FILMS_HASH_NAME,
                key=slug,
            ),
        )

    def create(self, film_create: FilmCreate) -> Film:
        film = Film(
            **film_create.model_dump(),
        )
        self.save_film_data(film)
        log.info("film created: %s", film.slug)
        return film

    def create_or_raise_if_exists(self, film_in: FilmCreate) -> Film:
        if not self.exists(film_in.slug):
            return self.create(film_in)
        raise FilmAlreadyExistsError(film_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_FILMS_HASH_NAME,
            slug,
        )
        log.info("film deleted: %s", slug)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(
        self,
        film: Film,
        film_in: FilmUpdate,
    ) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)
        self.save_film_data(film)
        log.info("film updated: %s", film.slug)
        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmPartialUpdate,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)
        self.save_film_data(film)
        log.info("film partial updated: %s", film.slug)
        return film


storage = FilmsStorage()
