from typing import Annotated

from annotated_types import Len, Ge, Le
from pydantic import BaseModel


SlugString = Annotated[
    str,
    Len(min_length=3, max_length=50),
]
TitleString = Annotated[
    str,
    Len(min_length=3, max_length=25),
]
DescriptionString = Annotated[
    str,
    Len(min_length=3, max_length=150),
]
YearString = Annotated[
    int,
    Ge(1900),
    Le(2050),
]
DurationMinutesString = Annotated[
    int,
    Ge(5),
    Le(5000),
]


class FilmBase(BaseModel):
    title: str
    description: str
    year: int
    duration_minutes: int


class FilmCreate(BaseModel):
    """
    Модель для создания фильма
    """

    slug: SlugString
    title: TitleString
    description: DescriptionString
    year: YearString
    duration_minutes: DurationMinutesString


class FilmUpdate(FilmBase):
    """
    Модель для обновления информации о фильме
    """

    title: TitleString
    description: DescriptionString
    year: YearString
    duration_minutes: DurationMinutesString


class FilmPartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации о фильме
    """

    title: TitleString | None = None
    description: DescriptionString | None = None
    year: YearString | None = None
    duration_minutes: DurationMinutesString | None = None


class FilmRead(FilmBase):
    """
    Модель для чтения данных о фильме
    """

    slug: str


class Film(FilmBase):
    """
    Модель фильма
    """

    slug: str
    notes: str = "some notes"
