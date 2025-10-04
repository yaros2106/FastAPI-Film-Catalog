class FilmBaseError(Exception):
    """
    Base exception class for film related errors.
    """


class FilmAlreadyExistsError(FilmBaseError):
    """
    Raised when a film on creation already exists.
    """
