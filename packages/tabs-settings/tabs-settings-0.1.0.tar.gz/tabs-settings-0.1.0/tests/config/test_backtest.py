from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.backtest import BacktestConfig
from tabs_settings.config.exchange_type import ExchangeType


def test_backtest_config_from_yaml():
    assert BacktestConfig.from_yaml(
        {
            "initial_portfolios": {
                "binance": {
                    "spot": {
                        "collateral_available": 600,
                        "collateral_allocated": 0,
                        "leverage": 20,
                    },
                    "future": {
                        "collateral_available": 600,
                        "collateral_allocated": 0,
                        "leverage": 20,
                    },
                },
            }
        }
    ).initial_portfolios == {
        ExchangeType.BINANCE: {
            AssetType.SPOT: {
                "collateral_available": 600,
                "collateral_allocated": 0,
                "leverage": 20,
            },
            AssetType.FUTURE: {
                "collateral_available": 600,
                "collateral_allocated": 0,
                "leverage": 20,
            },
        },
    }


def test_backtest_config_as_yaml():
    yaml_dict = {
        "initial_portfolios": {
            "binance": {
                "spot": {
                    "collateral_available": 600,
                    "collateral_allocated": 0,
                    "leverage": 20,
                },
                "future": {
                    "collateral_available": 600,
                    "collateral_allocated": 0,
                    "leverage": 20,
                },
            },
        }
    }
    assert BacktestConfig.from_yaml(yaml_dict).as_yaml == yaml_dict
