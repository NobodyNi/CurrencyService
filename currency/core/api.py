from fastapi import APIRouter

from ..schemas.schemas import CurrencySchema
from .memory import currencies

from .rates import get_exchange_rates

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/rub/get", summary='Получить рубль')
async def get_rub():
    logger.info("Запрос на получение значения RUB")
    return {"name": "RUB", "value": currencies.get("RUB")}


@router.get("/usd/get", summary='Получить доллар')
async def get_usd():
    logger.info("Запрос на получение значения USD")
    return {"name": "USD", "value": currencies.get("USD")}


@router.get("/eur/get", summary='Получить евро')
async def get_eur():
    logger.info("Запрос на получение значения EUR")
    return {"name": "EUR", "value": currencies.get("EUR")}


@router.get("/amount/get", summary='Общая сумма средств')
async def get_amount():
    logger.info("Запрос общей суммы средств")
    rates = await get_exchange_rates()

    rub_usd = rates["USD"]  # 1 USD = X RUB
    rub_eur = rates["EUR"]  # 1 EUR = Y RUB
    usd_eur = rub_usd / rub_eur

    usd_value = currencies.get("USD")
    eur_value = currencies.get("EUR")
    rub_value = currencies.get("RUB")

    # Общая сумма в рублях
    total_rub = rub_value + usd_value * rub_usd + eur_value * rub_eur

    return {
        "rub": rub_value,
        "usd": usd_value,
        "eur": eur_value,

        "rub-usd": rub_usd,
        "rub-eur": rub_eur,
        "usd-eur": usd_eur,

        "sum": f"{total_rub:.2f} rub / {total_rub / rub_usd:.2f} usd / {total_rub / rub_eur:.2f} eur"
    }


@router.post("/amount/set", summary='Установить новое значение')
async def set_amount(currency: CurrencySchema):
    updates = currency.model_dump(exclude_unset=True)
    logger.info(f"Запрос на установку значений: {updates}")

    for key, value in updates.items():
        currencies.set(key.upper(), value)

    logger.info(f"Установлено новое значение: {currencies.all()}")
    return {"message": "Установлено новое значение"}


@router.post("/modify", summary='Добавить, уменьшить к текущему значению')
async def modify_amount(currency: CurrencySchema):
    updates = currency.model_dump(exclude_unset=True)
    logger.info(f"Запрос на изменение значений: {updates}")

    for key, value in updates.items():
        currencies.modify(key.upper(), value)

    logger.info(f"Значение валюты изменено: {currencies.all()}")
    return {"message": "Значение валюты изменено"}
