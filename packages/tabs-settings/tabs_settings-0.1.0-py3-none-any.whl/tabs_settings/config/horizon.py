from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Horizon:
    name: str

    @classmethod
    def from_yaml(cls, horizon: str) -> Horizon:
        return cls(horizon)

    @property
    def as_yaml(self) -> str:
        return self.name

    def __lt__(self, other: Horizon) -> bool:
        return self.as_nanoseconds < other.as_nanoseconds

    @property
    def _value_and_unit(self) -> tuple[int, str]:
        # Use a regular expression to match a number followed by a unit
        match = re.match(r"(\d+)(ms|s|m|h)", self.name)
        if match is None:
            raise ValueError(f"Invalid input: {self.name}")

        # Extract the value and unit from the match
        value = int(match.group(1))
        unit = match.group(2)
        return value, unit

    @property
    def as_nanoseconds(self) -> int:
        value, unit = self._value_and_unit
        if unit == "ms":
            return value * 10**6
        elif unit == "s":
            return value * 10**9
        elif unit == "m":
            return value * 10**9 * 60
        elif unit == "h":
            return value * 10**9 * 60 * 60
        else:
            raise ValueError(f"Invalid time unit: {unit}")
