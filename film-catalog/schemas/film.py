from pydantic import BaseModel


class FilmBase(BaseModel):
    film_id: int
    title: str
    description: str
    year: int
    duration_minutes: int


class Film(FilmBase):
    """
    Модель фильма
    """
