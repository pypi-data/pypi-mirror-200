import pytest

from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.maturity import Maturity
from tabs_settings.config.ticker import Ticker
from tabs_settings.config.trading_pair import TradingPair


@pytest.mark.parametrize(
    "_dict, expected",
    [
        (
            {
                "base_asset": "BTC",
                "quote_asset": "USDT",
                "asset_type": "spot",
                "exchange": "binance",
                "is_active": True,
            },
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
        ),
        (
            {
                "base_asset": "BTC",
                "quote_asset": "USDT",
                "asset_type": "future",
                "exchange": "binance",
                "maturity": "20230331",
                "is_active": True,
            },
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity("20230331"),
            ),
        ),
        (
            {
                "base_asset": "BTC",
                "quote_asset": "USDT",
                "asset_type": "future",
                "exchange": "binance",
                "is_active": False,
            },
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                False,
                Maturity(),
            ),
        ),
    ],
)
def test_trading_pair_from_yaml(_dict: dict[str, str], expected: TradingPair) -> None:
    trading_pair = TradingPair.from_yaml(_dict)
    assert trading_pair == expected


@pytest.mark.parametrize(
    "trading_pair, expected",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            {
                "base_asset": "BTC",
                "quote_asset": "USDT",
                "asset_type": "spot",
                "exchange": "binance",
                "is_active": True,
            },
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity("20230331"),
            ),
            {
                "base_asset": "BTC",
                "quote_asset": "USDT",
                "asset_type": "future",
                "exchange": "binance",
                "is_active": True,
                "maturity": "20230331",
            },
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                False,
                Maturity(),
            ),
            {
                "base_asset": "BTC",
                "quote_asset": "USDT",
                "asset_type": "future",
                "exchange": "binance",
                "is_active": False,
            },
        ),
    ],
)
def test_trading_pair_to_yaml(trading_pair: TradingPair, expected: dict) -> None:
    assert trading_pair.as_yaml == expected


@pytest.mark.parametrize(
    "trading_pair",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                False,
            )
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity("20230331"),
            )
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity(),
            )
        ),
    ],
)
def test_trading_pair_serialisation_round_trip(trading_pair: TradingPair) -> None:
    serialised = trading_pair.as_yaml
    deserialised = TradingPair.from_yaml(serialised)
    assert trading_pair == deserialised


@pytest.mark.parametrize(
    "base_asset, quote_asset, asset_type, exchange, is_active, maturity, expected",
    [
        ("BTC", "USDT", "spot", "binance", True, None, "BINANCE_SPOT_BTC_USDT"),
        (
            "BTC",
            "USDT",
            "future",
            "binance",
            True,
            None,
            "BINANCE_FUTURE_BTC_USDT",
        ),
        (
            "BTC",
            "USDT",
            "future",
            "binance",
            True,
            "20230331",
            "BINANCE_FUTURE_BTC_USDT_20230331",
        ),
        ("BTC", "USDT", "future", "binance", True, None, "BINANCE_FUTURE_BTC_USDT"),
    ],
)
def test_trading_pair_from_parameters(
    base_asset: str,
    quote_asset: str,
    asset_type: str,
    exchange: str,
    is_active: bool,
    maturity: str | None,
    expected: str,
) -> None:
    trading_pair = TradingPair.from_parameters(
        base_asset, quote_asset, asset_type, exchange, is_active, maturity
    )
    assert trading_pair.full_name == expected


@pytest.mark.parametrize(
    "trading_pair, expected",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            "BINANCE_SPOT_BTC_USDT",
        ),
        (
            TradingPair(
                Ticker("ETH"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            "BINANCE_SPOT_ETH_USDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.KRAKEN,
                True,
                Maturity("20230331"),
            ),
            "KRAKEN_FUTURE_BTC_USDT_20230331",
        ),
    ],
)
def test_trading_pair_full_name(trading_pair: TradingPair, expected: str) -> None:
    assert trading_pair.full_name == expected


@pytest.mark.parametrize(
    "trading_pair, expected",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            "BTC/USDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity(),
            ),
            "BTC/USDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.KRAKEN,
                True,
            ),
            "BTC/USDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.KRAKEN,
                True,
                Maturity(),
            ),
            "BTC/USDT",
        ),
    ],
)
def test_ccxt_name(trading_pair: TradingPair, expected: str) -> None:
    assert trading_pair.ccxt_name == expected


@pytest.mark.parametrize(
    "trading_pair, expected",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            "BTCUSDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity(),
            ),
            "BTCUSDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity("20230331"),
            ),
            "BTCUSDT_230331",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.KRAKEN,
                True,
            ),
            "BTC/USDT",
        ),
        # (
        #     TradingPair(
        #         Ticker("BTC"),
        #         Ticker("USDT"),
        #         AssetType.FUTURE,
        #         ExchangeType.KRAKEN,
        #         Maturity(),
        #     ),
        #     "pf_btcusdt_perpetual",
        # ),
    ],
)
def test_exchange_name(trading_pair: TradingPair, expected: str) -> None:
    assert trading_pair.exchange_name == expected


@pytest.mark.parametrize(
    "trading_pair, expected",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            "BTCUSDT",
        ),
    ],
)
def test_trading_pair_name(trading_pair: TradingPair, expected: str) -> None:
    assert trading_pair.pair_name == expected


@pytest.mark.parametrize(
    "trading_pair, expected",
    [
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.SPOT,
                ExchangeType.BINANCE,
                True,
            ),
            "BTCUSDT",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity("20230331"),
            ),
            "BTCUSDT_20230331",
        ),
        (
            TradingPair(
                Ticker("BTC"),
                Ticker("USDT"),
                AssetType.FUTURE,
                ExchangeType.BINANCE,
                True,
                Maturity(),
            ),
            "BTCUSDT",
        ),
    ],
)
def test_trading_pair_name_maybe_with_maturity(
    trading_pair: TradingPair, expected: str
) -> None:
    assert trading_pair.pair_name_maybe_with_maturity == expected


@pytest.mark.parametrize(
    "trading_pair_1, trading_pair_2",
    [
        (
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
                "spot",
                "kraken",
                True,
            ),
        ),
        (
            TradingPair.from_parameters(
                "BTC",
                "USDT",
                "future",
                "binance",
                True,
            ),
            TradingPair.from_parameters(
                "BTC",
                "USDT",
                "spot",
                "binance",
                True,
            ),
        ),
        (
            TradingPair.from_parameters(
                "BTC",
                "ETH",
                "future",
                "binance",
                True,
            ),
            TradingPair.from_parameters(
                "BTC",
                "USDT",
                "future",
                "binance",
                True,
            ),
        ),
        (
            TradingPair.from_parameters("BTC", "USDT", "future", "binance", True),
            TradingPair.from_parameters(
                "BTC", "USDT", "future", "binance", True, "20230331"
            ),
        ),
    ],
)
def test_trading_pair_lt(
    trading_pair_1: TradingPair, trading_pair_2: TradingPair
) -> None:
    assert trading_pair_1 < trading_pair_2
