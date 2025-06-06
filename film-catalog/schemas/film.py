from typing import Annotated

from annotated_types import Len, Ge, Le
from pydantic import BaseModel


class FilmBase(BaseModel):
    slug: str
    title: str
    description: str
    year: int
    duration_minutes: int


class FilmCreateBase(BaseModel):
    # noinspection PyTypeHints
    slug: Annotated[
        str,
        Len(min_length=3, max_length=50),
    ]
    # noinspection PyTypeHints
    title: Annotated[
        str,
        Len(min_length=3, max_length=25),
    ]
    # noinspection PyTypeHints
    description: Annotated[
        str,
        Len(min_length=3, max_length=150),
    ]
    year: Annotated[
        int,
        Ge(1900),
        Le(2050),
    ]
    duration_minutes: Annotated[
        int,
        Ge(5),
        Le(5000),
    ]


class FilmCreate(FilmCreateBase):
    """
    Модель для создания фильма
    """


class Film(FilmBase):
    """
    Модель фильма
    """
