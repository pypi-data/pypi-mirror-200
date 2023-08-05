from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Maturity:
    date: str | None = None  # perpetual is None

    @property
    def name(self) -> str | None:
        return self.date

    @classmethod
    def from_settings(cls, maturity: str | int | None) -> Maturity:
        # perpetual is None
        if maturity is not None:
            maturity = str(maturity)
            try:
                if not Maturity.is_last_friday_of_month(maturity):
                    raise ValueError("Not the last Friday of the month")
                return cls(maturity)
            except ValueError:
                raise ValueError("Invalid maturity string")
        return cls(None)

    @staticmethod
    def is_last_friday_of_month(maturity: str) -> bool:
        date = datetime.strptime(maturity, "%Y%m%d")
        if date.weekday() != 4:  # Check if date is a Friday (weekday 4)
            return False
        next_friday = date + timedelta(days=7)
        return next_friday.month != date.month

    @property
    def exchange_name(self) -> str | None:
        if not self.is_perpetual:
            assert self.date is not None
            return self.date[2:]  # encoded as YYMMDD

    @property
    def is_perpetual(self) -> bool:
        return self.date is None
