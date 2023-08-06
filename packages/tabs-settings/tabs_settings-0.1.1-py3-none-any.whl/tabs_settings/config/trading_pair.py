from __future__ import annotations

from dataclasses import dataclass

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.maturity import Maturity
from tabs_settings.config.ticker import Ticker


@dataclass(frozen=True)
class TradingPair:
    base_asset: Ticker
    quote_asset: Ticker
    asset_type: AssetType
    exchange: ExchangeType
    is_active: bool = True
    maturity: Maturity | None = None

    @classmethod
    def from_yaml(cls, settings: dict[str, str | bool]) -> TradingPair:
        return cls.from_parameters(**settings)

    @property
    def as_yaml(self) -> dict[str, str | bool]:
        _dict = {
            "base_asset": str(self.base_asset),
            "quote_asset": str(self.quote_asset),
            "asset_type": str(self.asset_type),
            "exchange": str(self.exchange),
            "is_active": self.is_active,
        }
        if self.maturity is not None and not self.maturity.is_perpetual:
            _dict["maturity"] = self.maturity.name
        return _dict

    @classmethod
    def from_parameters(
        cls,
        base_asset: str,
        quote_asset: str,
        asset_type: str,
        exchange: str,
        is_active: bool = True,
        maturity: str | int | None = None,
    ) -> TradingPair:
        asset_type_obj = AssetType.from_settings(asset_type)
        if asset_type_obj is AssetType.SPOT:
            assert maturity is None

        maturity_obj = None
        if asset_type_obj is AssetType.FUTURE:
            maturity_obj = Maturity.from_settings(maturity)

        return cls(
            Ticker(base_asset),
            Ticker(quote_asset),
            asset_type_obj,
            ExchangeType.from_settings(exchange),
            is_active,
            maturity_obj,
        )

    # implement method that allow to compare two trading pairs.
    # this method is used to enfore an order in the trading pairs list
    def __lt__(self, other: TradingPair) -> bool:
        return self.full_name < other.full_name

    ### Various names for the trading pair ###

    @property
    def full_name(self) -> str:
        result = (
            f"{self.exchange}_{self.asset_type}_{self.base_asset}_{self.quote_asset}"
        )
        if self.maturity is not None and not self.maturity.is_perpetual:
            result += f"_{self.maturity.date}"
        return result.upper()

    @property
    def pair_name(self) -> str:
        return f"{self.base_asset}{self.quote_asset}"

    @property
    def pair_name_maybe_with_maturity(self) -> str:
        result = self.pair_name
        if self.maturity is not None and not self.maturity.is_perpetual:
            result += f"_{self.maturity.date}"
        return result

    @property
    def ccxt_name(self) -> str:
        return f"{self.base_asset}/{self.quote_asset}"

    @property
    def exchange_name(self) -> str:
        if self.exchange is ExchangeType.KRAKEN and self.asset_type is AssetType.FUTURE:
            result = f"pf_{str(self.base_asset).lower()}{str(self.quote_asset).lower()}"
        elif self.exchange is ExchangeType.BINANCE:
            result = f"{self.base_asset}{self.quote_asset}"
        else:
            result = f"{self.base_asset}/{self.quote_asset}"

        if (
            self.exchange is ExchangeType.BINANCE
            and self.asset_type is AssetType.FUTURE
        ):
            if self.maturity is not None and not self.maturity.is_perpetual:
                result += f"_{self.maturity.exchange_name}"

        return result
