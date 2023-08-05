import pytest

from tabs_settings.config.exchange_type import ExchangeType


@pytest.mark.parametrize(
    "exchange, expected",
    [
        (ExchangeType.BINANCE, "binance"),
        (ExchangeType.KRAKEN, "kraken"),
    ],
)
def test_exchange_str(exchange: ExchangeType, expected: str) -> None:
    assert str(exchange) == expected
