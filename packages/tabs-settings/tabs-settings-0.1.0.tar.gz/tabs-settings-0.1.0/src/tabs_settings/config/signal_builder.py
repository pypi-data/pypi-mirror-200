from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalBuilderConfig:
    windows_size: tuple[int, ...]
    levels: tuple[int, ...]

    @classmethod
    def from_yaml(cls, settings: dict) -> SignalBuilderConfig:
        """
        windows_size:
            - 10
            - 50
            - 260
            - 500
            - 1000
            - 2000
        levels:
            - 0
            - 1
        """
        return cls(tuple(settings["windows_size"]), tuple(settings["levels"]))

    @property
    def as_yaml(self) -> dict:
        return {"windows_size": list(self.windows_size), "levels": list(self.levels)}
