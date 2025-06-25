import logging

from pydantic import (
    BaseModel,
    ValidationError,
)
from redis import Redis

from core import config
from core.config import FILM_STORAGE_FILEPATH
from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmPartialUpdate,
)


log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmsStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}

    def save_state(self) -> None:
        FILM_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("saved state films to storage file")

    @classmethod
    def load_state(cls) -> "FilmsStorage":
        if not FILM_STORAGE_FILEPATH.exists():
            log.info("film storage file doesn't exist")
            return FilmsStorage()
        return cls.model_validate_json(FILM_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = FilmsStorage.load_state()
        except ValidationError as e:
            self.save_state()
            log.warning(
                "Rewritten film storage file due to validation error: %s", str(e)
            )
            return

        # если будут новые свойства,
        # то их тоже придется обновить напрямую
        self.slug_to_film.update(
            data.slug_to_film,
        )
        log.warning("film storage loaded")

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

    def create(self, film_crate: FilmCreate) -> Film:
        film = Film(
            **film_crate.model_dump(),
        )
        self.save_film_data(film)
        log.info("film created: %s", film.slug)
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)
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
