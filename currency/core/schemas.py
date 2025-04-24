from pydantic import BaseModel
from typing import Optional


class CurrencySchema(BaseModel):
    usd: Optional[float] = None
    rub: Optional[float] = None
    eur: Optional[float] = None
