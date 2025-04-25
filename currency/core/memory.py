from ..base.abstract import AbstractCurrency


class MemoryCurrency(AbstractCurrency):
    def __init__(self, initial=None):
        self._currencies = initial or {"USD": 0.0, "RUB": 0.0, "EUR": 0.0}

    def get(self, currency: str) -> float:
        return self._currencies.get(currency.upper(), 0.0)

    def set(self, currency: str, value: float) -> None:
        self._currencies[currency.upper()] = value

    def modify(self, currency: str, value: float) -> None:
        self._currencies[currency.upper()] += value

    def all(self):
        return self._currencies.copy()


currencies = MemoryCurrency()
