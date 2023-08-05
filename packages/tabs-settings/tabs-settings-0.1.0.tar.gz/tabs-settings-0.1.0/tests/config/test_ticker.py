import pytest

from tabs_settings.config.ticker import Ticker


@pytest.mark.parametrize(
    "ticker, expected",
    [
        (Ticker("BTC"), "BTC"),
        (Ticker("ETH"), "ETH"),
        (Ticker("ADA"), "ADA"),
    ],
)
def test_ticker_str(ticker: Ticker, expected: str) -> None:
    assert str(ticker) == expected
