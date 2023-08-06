import pytest
from immutables import Map

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.fee import Fee
from tabs_settings.config.trading_pair import TradingPair


@pytest.fixture
def exchange_fee_settings() -> Map:
    return Map(
        {
            "binance": {
                "future": {
                    "taker": 0.05,
                    "maker": 0.01,
                },
                "spot": {
                    "taker": 0.1,
                    "maker": 0.05,
                },
            },
            "kraken": {
                "future": {
                    "taker": 0.1,
                    "maker": 0.02,
                },
                "spot": {
                    "taker": 0.2,
                    "maker": 0.04,
                },
            },
        }
    )


def test_fee_from_yaml(exchange_fee_settings: Map) -> None:
    expected_fee = {
        ExchangeType.BINANCE: {
            AssetType.FUTURE: {
                "taker": 0.05,
                "maker": 0.01,
            },
            AssetType.SPOT: {
                "taker": 0.1,
                "maker": 0.05,
            },
        },
        ExchangeType.KRAKEN: {
            AssetType.FUTURE: {
                "taker": 0.1,
                "maker": 0.02,
            },
            AssetType.SPOT: {
                "taker": 0.2,
                "maker": 0.04,
            },
        },
    }
    fee = Fee.from_yaml(exchange_fee_settings)
    assert fee.fees == Map(expected_fee)


def test_as_yaml(exchange_fee_settings: Map) -> None:
    expected_fee = {
        "binance": {
            "future": {
                "taker": 0.05,
                "maker": 0.01,
            },
            "spot": {
                "taker": 0.1,
                "maker": 0.05,
            },
        },
        "kraken": {
            "future": {
                "taker": 0.1,
                "maker": 0.02,
            },
            "spot": {
                "taker": 0.2,
                "maker": 0.04,
            },
        },
    }
    fee = Fee.from_yaml(exchange_fee_settings)
    assert fee.as_yaml == expected_fee


@pytest.mark.parametrize(
    "trading_pair, expected_taker, expected_maker",
    [
        (
            TradingPair.from_parameters(
                "BTC",
                "USDT",
                "future",
                "binance",
            ),
            0.05,
            0.01,
        ),
    ],
)
def test_fees_taker_maker(
    exchange_fee_settings: Map, trading_pair, expected_taker, expected_maker
) -> None:
    fee = Fee.from_yaml(exchange_fee_settings)
    assert fee.taker(trading_pair) == expected_taker
    assert fee.maker(trading_pair) == expected_maker
