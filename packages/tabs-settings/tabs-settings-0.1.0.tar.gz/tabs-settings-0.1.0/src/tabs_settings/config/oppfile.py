from __future__ import annotations

from dataclasses import dataclass

from tabs_settings.config.horizon import Horizon
from tabs_settings.config.signal_builder import SignalBuilderConfig


@dataclass(frozen=True)
class OppfileConfig:
    signal_builder: SignalBuilderConfig
    deadspaces: tuple[Horizon, ...]
    fillsims: tuple[Horizon, ...]
    horizons: tuple[Horizon, ...]
    fees: tuple[float, ...]

    @classmethod
    def from_yaml(cls, settings: dict) -> OppfileConfig:
        """
        signal_builder:
            # per cell and side
            # trades price diff
            # top of book price diff
            # top of book quantity (cumsum up to depth)

            # per trading_pair
            # direction (mean of signed quantity)
            # volume (sum of signed quantity)
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
            - 2
            - 3

        deadspaces:
            - 1ms

        fillsims:
            - 0ms
            - 10ms

        horizons:
            - 100ms
            - 1s

        fees:
            - 0
            - 0.0004
        """
        return cls(
            SignalBuilderConfig.from_yaml(settings["signal_builder"]),
            tuple(sorted(tuple(Horizon.from_yaml(h) for h in settings["deadspaces"]))),
            tuple(sorted(tuple(Horizon.from_yaml(h) for h in settings["fillsims"]))),
            tuple(sorted(tuple(Horizon.from_yaml(h) for h in settings["horizons"]))),
            tuple(sorted(tuple(float(f) for f in settings["fees"]))),
        )

    @property
    def as_yaml(self) -> dict:
        return {
            "signal_builder": self.signal_builder.as_yaml,
            "deadspaces": [h.as_yaml for h in sorted(self.deadspaces)],
            "fillsims": [h.as_yaml for h in sorted(self.fillsims)],
            "horizons": [h.as_yaml for h in sorted(self.horizons)],
            "fees": [f for f in sorted(self.fees)],
        }
