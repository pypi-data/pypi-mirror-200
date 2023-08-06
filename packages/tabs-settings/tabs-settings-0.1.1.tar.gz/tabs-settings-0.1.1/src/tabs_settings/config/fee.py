from __future__ import annotations

from dataclasses import dataclass

from immutables import Map

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.trading_pair import TradingPair


@dataclass(frozen=True)
class Fee:
    fees: Map

    @classmethod
    def from_yaml(
        cls,
        exchange_fee_settings: Map,
    ) -> Fee:
        """
        binance:
            future:
              maker: 0.0002
              taker: 0.0004
            spot:
              maker: 0
              taker: 0
        kraken:
            future:
              maker: 0.0002
              taker: 0.0005
            spot:
              maker: 0
              taker: 0
        """

        # interpret exchange and asset type from the settings
        processed_fees = {}
        for exchange, asset_types in exchange_fee_settings.items():
            exchange_obj = ExchangeType.from_settings(exchange)
            processed_fees[exchange_obj] = {}
            for asset_type, fees in asset_types.items():
                asset_type_obj = AssetType.from_settings(asset_type)
                processed_fees[exchange_obj][asset_type_obj] = fees
        return cls(Map(processed_fees))

    @property
    def as_yaml(self) -> dict:
        # convert the exchange and asset_type objects back to strings
        processed_fees = {}
        for exchange, asset_types in self.fees.items():
            processed_fees[exchange.name.lower()] = {}
            for asset_type, fees in asset_types.items():
                processed_fees[exchange.name.lower()][asset_type.name.lower()] = fees
        return processed_fees

    def taker(self, trading_pair: TradingPair) -> float:
        return self.fees[trading_pair.exchange][trading_pair.asset_type]["taker"]

    def maker(self, trading_pair: TradingPair) -> float:
        return self.fees[trading_pair.exchange][trading_pair.asset_type]["maker"]
