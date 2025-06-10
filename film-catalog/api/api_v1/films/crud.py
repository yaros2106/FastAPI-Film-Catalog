from pydantic import BaseModel

from schemas.film import Film, FilmCreate, FilmUpdate, FilmPartialUpdate


class FilmsStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, film_crate: FilmCreate) -> Film:
        film = Film(
            **film_crate.model_dump(),
        )
        self.slug_to_film[film.slug] = film
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(
        self,
        film: Film,
        film_in: FilmUpdate,
    ) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)
        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmPartialUpdate,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)
        return film


storage = FilmsStorage()

storage.create(
    FilmCreate(
        slug="the-walking-dead",
        title="The Walking Dead",
        description="A group of survivors navigates a post-apocalyptic world overrun by zombies",
        year=2010,
        duration_minutes=44,
    )
)
storage.create(
    FilmCreate(
        slug="outcast",
        title="outcast",
        description="After a plane crash, a FedEx executive struggles to survive on a deserted island",
        year=2000,
        duration_minutes=143,
    )
)
storage.create(
    FilmCreate(
        slug="the-matrix",
        title="The Matrix",
        description="A computer hacker learns about the true nature of his reality and his role in the war against its controllers",
        year=1999,
        duration_minutes=136,
    )
)
