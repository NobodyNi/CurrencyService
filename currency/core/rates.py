import asyncio
import logging
import httpx

from .memory import currencies

logger = logging.getLogger(__name__)

URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def get_exchange_rates(base: str = "RUB", symbols: str = "USD,EUR") -> dict:
    """
    Получает курсы валют относительно базовой валюты (по умолчанию RUB).
    Возвращает словарь с курсами.
    """
    params = {"base": base, "symbols": symbols}

    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Отправка запроса: {URL} с параметрами {params}")
            response = await client.get(URL, params=params)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"Получен ответ: {response.status_code}")

            rates = {
                "USD": data["Valute"]["USD"]["Value"],
                "EUR": data["Valute"]["EUR"]["Value"]
            }
            return rates

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP ошибка при получении курсов валют: {e}")
    except httpx.RequestError as e:
        logger.error(f"Ошибка соединения при запросе курсов валют: {e}")

        return {}


async def update_rates(args):
    """
    Периодически обновляет и логирует информацию о курсах валют и общих балансах.
    """
    last_rates = None
    last_balances = None
    last_total = None

    while True:
        try:
            rates = await get_exchange_rates()

            current_balances = currencies.all()

            rub = currencies.get("RUB")
            usd = currencies.get("USD")
            eur = currencies.get("EUR")

            rub_usd = rates["USD"]
            rub_eur = rates["EUR"]
            usd_eur = rub_usd / rub_eur

            total_rub = rub + usd * rub_usd + eur * rub_eur

            # проверяем не изменилось ли что
            if (rates != last_rates or
                    current_balances != last_balances or
                    total_rub != last_total):
                logger.info(
                    f"\n"
                    f"rub: {rub}\n"
                    f"usd: {usd}\n"
                    f"eur: {eur}\n\n"
                    f"rub-usd: {rub_usd}\n"
                    f"rub-eur: {rub_eur}\n"
                    f"usd-eur: {usd_eur:.2f}\n\n"
                    f"sum: {total_rub:.2f} rub / {total_rub / rub_usd:.2f} usd / {total_rub / rub_eur:.2f} eur\n"
                )

                # обновляем значения
                last_rates = rates
                last_balances = current_balances
                last_total = total_rub

        except Exception as e:
            logger.exception("Ошибка при обновлении курсов валют или расчете суммы")

        await asyncio.sleep(args.period * 60)
