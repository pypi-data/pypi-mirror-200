import pytest

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.basket import Basket
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.trading_pair import TradingPair


@pytest.mark.parametrize(
    "basket_dict, expected",
    [
        (
            {
                "name": "ETHUSDT-ADAUSDT",
                "trading_pairs": {
                    "binance": {
                        "spot": [
                            {
                                "base_asset": "BTC",
                                "quote_asset": "USDT",
                                "is_active": True,
                            },
                            {
                                "base_asset": "ETH",
                                "quote_asset": "USDT",
                                "is_active": True,
                            },
                        ],
                        "future": [
                            {
                                "base_asset": "BTC",
                                "quote_asset": "USDT",
                                "is_active": True,
                                "maturity": "20211231",
                            },
                            {
                                "base_asset": "ETH",
                                "quote_asset": "USDT",
                                "is_active": True,
                                "maturity": "20211231",
                            },
                        ],
                    },
                    "kraken": {
                        "spot": [
                            {
                                "base_asset": "BTC",
                                "quote_asset": "USDT",
                                "is_active": True,
                            },
                            {
                                "base_asset": "ETH",
                                "quote_asset": "USDT",
                                "is_active": True,
                            },
                        ]
                    },
                },
            },
            Basket(
                name="ETHUSDT-ADAUSDT",
                trading_pairs=frozenset(
                    [
                        TradingPair.from_parameters(
                            "ETH",
                            "USDT",
                            "future",
                            "binance",
                            True,
                            "20211231",
                        ),
                        TradingPair.from_parameters(
                            "BTC",
                            "USDT",
                            "spot",
                            "binance",
                            True,
                        ),
                        TradingPair.from_parameters(
                            "BTC",
                            "USDT",
                            "future",
                            "binance",
                            True,
                            "20211231",
                        ),
                        TradingPair.from_parameters(
                            "BTC", "USDT", "spot", "kraken", True
                        ),
                        TradingPair.from_parameters(
                            "ETH", "USDT", "spot", "binance", True
                        ),
                        TradingPair.from_parameters(
                            "ETH", "USDT", "spot", "kraken", True
                        ),
                    ]
                ),
            ),
        ),
    ],
)
def test_basket_from_yaml(basket_dict, expected):
    assert Basket.from_yaml(basket_dict) == expected


@pytest.mark.parametrize(
    "basket, expected",
    [
        (
            Basket(
                name="ETHUSDT-ADAUSDT",
                trading_pairs=frozenset(
                    [
                        TradingPair.from_parameters("BTC", "USDT", "spot", "binance"),
                        TradingPair.from_parameters("ETH", "USDT", "spot", "binance"),
                        TradingPair.from_parameters(
                            "BTC",
                            "USDT",
                            "future",
                            "binance",
                            True,
                        ),
                        TradingPair.from_parameters(
                            "ETH",
                            "USDT",
                            "future",
                            "kraken",
                            True,
                        ),
                    ]
                ),
            ),
            {
                ExchangeType.BINANCE: {
                    AssetType.SPOT: frozenset(
                        [
                            TradingPair.from_parameters(
                                "BTC", "USDT", "spot", "binance", True
                            ),
                            TradingPair.from_parameters(
                                "ETH", "USDT", "spot", "binance", True
                            ),
                        ]
                    ),
                    AssetType.FUTURE: frozenset(
                        [
                            TradingPair.from_parameters(
                                "BTC",
                                "USDT",
                                "future",
                                "binance",
                                True,
                            ),
                        ]
                    ),
                },
                ExchangeType.KRAKEN: {
                    AssetType.FUTURE: frozenset(
                        [
                            TradingPair.from_parameters(
                                "ETH",
                                "USDT",
                                "future",
                                "kraken",
                                True,
                            ),
                        ]
                    ),
                },
            },
        ),
    ],
)
def test_basket_as_grouped_dict(basket, expected):
    assert basket.as_grouped_dict == expected


@pytest.mark.parametrize(
    "basket, expected",
    [
        (
            Basket(
                name="ETHUSDT-ADAUSDT",
                trading_pairs=frozenset(
                    [
                        TradingPair.from_parameters(
                            "BTC", "USDT", "spot", "binance", True
                        ),
                        TradingPair.from_parameters(
                            "ETH", "USDT", "spot", "binance", True
                        ),
                    ]
                ),
            ),
            {
                "name": "ETHUSDT-ADAUSDT",
                "trading_pairs": {
                    "binance": {
                        "spot": [
                            {
                                "base_asset": "BTC",
                                "quote_asset": "USDT",
                                "is_active": True,
                            },
                            {
                                "base_asset": "ETH",
                                "quote_asset": "USDT",
                                "is_active": True,
                            },
                        ]
                    }
                },
            },
        ),
    ],
)
def test_basket_as_yaml(basket, expected):
    assert basket.as_yaml == expected


def test_basket_yaml_round_trip():
    basket = {
        "name": "ETHUSDT-ADAUSDT",
        "trading_pairs": {
            "binance": {
                "spot": [
                    {"base_asset": "BTC", "quote_asset": "USDT", "is_active": True},
                    {"base_asset": "ETH", "quote_asset": "USDT", "is_active": True},
                ],
                "future": [
                    {
                        "base_asset": "BTC",
                        "quote_asset": "USDT",
                        "is_active": True,
                        "maturity": "20211231",
                    },
                    {
                        "base_asset": "ETH",
                        "quote_asset": "USDT",
                        "is_active": True,
                        "maturity": "20211231",
                    },
                ],
            },
            "kraken": {
                "spot": [
                    {"base_asset": "BTC", "quote_asset": "USDT", "is_active": True},
                    {"base_asset": "ETH", "quote_asset": "USDT", "is_active": True},
                ]
            },
        },
    }
    basket = Basket.from_yaml(basket)
    assert Basket.from_yaml(basket.as_yaml) == basket


@pytest.mark.parametrize(
    "basket, expected",
    [
        (
            Basket(
                name="ETHUSDT-ADAUSDT",
                trading_pairs=frozenset(
                    [
                        TradingPair.from_parameters(
                            "BTC", "USDT", "spot", "binance", True
                        ),
                        TradingPair.from_parameters(
                            "ETH", "USDT", "spot", "binance", True
                        ),
                    ]
                ),
            ),
            "ETHUSDT-ADAUSDT",
        ),
    ],
)
def test_basket_name(basket, expected):
    assert basket.name == expected
