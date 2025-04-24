import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .core.memory import currencies
from .core.api import router
from .config.config import parse_args, setup_logging
from .core.rates import update_rates

import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    args = parse_args()
    setup_logging(args.debug)

    currencies.set("RUB", args.rub)
    currencies.set("USD", args.usd)
    currencies.set("EUR", args.eur)

    logger.debug(f"Запуск с параметрами: {args}")

    logger.info("Приложение запущено успешно.")

    # запускаем фоновую задачу
    task = asyncio.create_task(update_rates(args))

    yield  # приложение работает

    # останавливаем фоновую задачу
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Фоновая задача update_rates остановлена.")


app = FastAPI(lifespan=lifespan)
app.include_router(router)