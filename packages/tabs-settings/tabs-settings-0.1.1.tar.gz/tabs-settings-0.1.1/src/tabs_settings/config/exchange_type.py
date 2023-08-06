from __future__ import annotations

from enum import IntEnum


class ExchangeType(IntEnum):
    BINANCE = 0
    KRAKEN = 1
    OKX = 2

    @classmethod
    def from_settings(cls, exchange: str) -> ExchangeType:
        return cls[exchange.upper()]

    def __str__(self) -> str:
        return self.name.lower()
