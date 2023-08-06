from __future__ import annotations

from dataclasses import dataclass

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.trading_pair import TradingPair


@dataclass(frozen=True)
class Basket:
    name: str
    trading_pairs: frozenset[TradingPair]

    def __iter__(self):
        return iter(self.trading_pairs)

    @classmethod
    def from_yaml(cls, settings: dict) -> Basket:
        """
        name: ETHUSDT-ADAUSDT
        trading_pairs:
            binance:
                future:
                    - base_asset: ETH
                    quote_asset: USDT
                    active: true
                    - base_asset: ETH
                    quote_asset: USDT
                    maturity: 20230331
                    active: true
                spot:
                    - base_asset: ETH
                    quote_asset: USDT
                    active: false
                    - base_asset: ADA
                    quote_asset: USDT
                    active: false
            kraken:
                future:
                    - base_asset: ETH
                    quote_asset: USDT
                    active: true
                    - base_asset: ETH
                    quote_asset: USDT
                    maturity: 20230331
                    active: true
                spot:
                    - base_asset: ETH
                    quote_asset: USDT
                    active: false
                    - base_asset: ADA
                    quote_asset: USDT
                    active: false
        """
        # load name
        name = settings["name"]

        # apply the from_yaml to each trading pair
        trading_pairs = []
        for exchange, asset_types in settings["trading_pairs"].items():
            for asset_type, pairs in asset_types.items():
                for pair in pairs:
                    enhanced_pair_description = pair.copy()
                    enhanced_pair_description["asset_type"] = asset_type
                    enhanced_pair_description["exchange"] = exchange
                    trading_pair = TradingPair.from_yaml(enhanced_pair_description)
                    trading_pairs.append(trading_pair)
        return cls(name, frozenset(trading_pairs))

    ### two kind of representation:
    # - as_yaml: for the yaml file
    # - as_dict: for the data download

    @property
    def as_grouped_dict(
        self,
    ) -> dict[ExchangeType, dict[AssetType, frozenset[TradingPair]]]:
        by_exchange = {}
        for trading_pair in self.trading_pairs:
            by_exchange.setdefault(trading_pair.exchange, {}).setdefault(
                trading_pair.asset_type, set()
            ).add(trading_pair)

        # convert all the sets to frozensets
        for _, by_asset_type in by_exchange.items():
            for asset_type, trading_pairs in by_asset_type.items():
                by_asset_type[asset_type] = frozenset(trading_pairs)
        return by_exchange

    @property
    def as_yaml(self) -> dict:
        grouped_dict = self.as_grouped_dict
        trading_pairs_dict = {}
        for exchange, by_asset_type in grouped_dict.items():
            trading_pairs_dict[str(exchange)] = {}
            for asset_type, trading_pairs in by_asset_type.items():
                trading_pairs_dict[str(exchange)][str(asset_type)] = []
                for trading_pair in sorted(trading_pairs):
                    trading_pair_yaml = trading_pair.as_yaml
                    del trading_pair_yaml["asset_type"]
                    del trading_pair_yaml["exchange"]
                    trading_pairs_dict[str(exchange)][str(asset_type)].append(
                        trading_pair_yaml
                    )
        return {"name": self.name, "trading_pairs": trading_pairs_dict}

    # implement lt and gt to allow sorting
    def __lt__(self, other: Basket) -> bool:
        return self.name < other.name
