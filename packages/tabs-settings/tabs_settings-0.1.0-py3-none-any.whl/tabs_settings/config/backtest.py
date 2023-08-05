from __future__ import annotations

from dataclasses import dataclass

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType


@dataclass(frozen=True)
class BacktestConfig:
    initial_portfolios: dict

    @classmethod
    def from_yaml(cls, settings: dict) -> BacktestConfig:
        """
        initial_portfolios:
            binance:
                spot:
                    collateral_available: 600
                    collateral_allocated: 0
                    leverage: 20
                future:
                    collateral_available: 600
                    collateral_allocated: 0
                    leverage: 20
            kraken:
                spot:
                    collateral_available: 600
                    collateral_allocated: 0
                    leverage: 20
                future:
                    collateral_available: 600
                    collateral_allocated: 0
                    leverage: 20
        """
        # interpret exchange and asset type from the settings
        initial_portfolio_settings = settings["initial_portfolios"]
        processed_initial_portfolios = {}
        for exchange, asset_types in initial_portfolio_settings.items():
            exchange_obj = ExchangeType.from_settings(exchange)
            processed_initial_portfolios[exchange_obj] = {}
            for asset_type, initial_portfolio in asset_types.items():
                asset_type_obj = AssetType.from_settings(asset_type)
                processed_initial_portfolios[exchange_obj][
                    asset_type_obj
                ] = initial_portfolio
        return cls(processed_initial_portfolios)

    @property
    def as_yaml(self) -> dict:
        processed_initial_portfolios = {}
        for exchange, asset_types in self.initial_portfolios.items():
            processed_initial_portfolios[exchange.name.lower()] = {}
            for asset_type, initial_portfolio in asset_types.items():
                processed_initial_portfolios[exchange.name.lower()][
                    asset_type.name.lower()
                ] = initial_portfolio
        return {"initial_portfolios": processed_initial_portfolios}
