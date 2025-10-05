from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.films import FilmsStorage


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None]:
    # действие до запуска приложения
    # noinspection PyUnresolvedReferences
    app.state.films_storage = FilmsStorage(
        hash_name=settings.redis.collection_name.films_hash,
    )
    # ставим эту функцию на паузу на время работы приложения
    yield
    # выполняем завершение работы,
    # закрываем соединение, финально все сохраняем
