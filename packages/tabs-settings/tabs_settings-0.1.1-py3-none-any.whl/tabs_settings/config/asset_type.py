from __future__ import annotations

from enum import IntEnum


class AssetType(IntEnum):
    SPOT = 0
    FUTURE = 1
    OPTION = 2

    @classmethod
    def from_settings(cls, asset_type: str) -> AssetType:
        return cls[asset_type.upper()]

    def __str__(self) -> str:
        return self.name.lower()
