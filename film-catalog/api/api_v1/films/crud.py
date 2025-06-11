from pydantic import (
    BaseModel,
    ValidationError,
)

from core.config import FILM_STORAGE_FILEPATH
from schemas.film import Film, FilmCreate, FilmUpdate, FilmPartialUpdate


class FilmsStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}

    def save_state(self) -> None:
        return FILM_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load_state(cls) -> "FilmsStorage":
        if not FILM_STORAGE_FILEPATH.exists():
            return FilmsStorage()
        return cls.model_validate_json(FILM_STORAGE_FILEPATH.read_text())

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, film_crate: FilmCreate) -> Film:
        film = Film(
            **film_crate.model_dump(),
        )
        self.slug_to_film[film.slug] = film
        self.save_state()
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)
        self.save_state()

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(
        self,
        film: Film,
        film_in: FilmUpdate,
    ) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)
        self.save_state()
        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmPartialUpdate,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)
        self.save_state()
        return film


try:
    storage = FilmsStorage().load_state()
except ValidationError:
    storage = FilmsStorage()
    storage.save_state()
