from dataclasses import dataclass


@dataclass(frozen=True)
class Threshold:
    buy: float
    sell: float
