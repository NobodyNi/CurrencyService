from abc import ABC, abstractmethod


class AbstractCurrency(ABC):
    """
    Абстрактный класс для работы с валютами

    Определяет методы получения, добавления/изменения
    баланса валюты
    """
    @abstractmethod
    def get(self, currency: str) -> float:
        """
        Получает текущий баланс указанной валюты
        """
        pass

    @abstractmethod
    def set(self, currency: str, value: float) -> None:
        """
        Уставливает начальный баланс для указанной валюты
        """
        pass

    @abstractmethod
    def modify(self, currency: str, value: float) -> None:
        """
        Изменяет баланс валюты на определенную величину
        """
        pass