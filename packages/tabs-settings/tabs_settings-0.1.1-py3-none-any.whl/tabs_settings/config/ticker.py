from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Ticker:
    name: str

    def __str__(self):
        return self.name
