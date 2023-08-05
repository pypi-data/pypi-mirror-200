import pytest
import yaml

from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.storage import PathFormatType, StorageConfig


@pytest.fixture
def storage_config_yaml():
    return yaml.safe_load(
        """
        path_format:
            raw_data: data/raw_data/{version}/{exchange}/{asset_type}/{trading_pair}/{data_segment}/{date}.{extension}
            oppfile: data/learn/{version}/dataset/{basket}/{data_segment}/{date}.{extension}
            learn: data/learn/{version}/{rolling_learn_id}/{learn_id}/{basket}/{data_segment}/{date}.{extension}

        extension:
            # raw data
            raw_trades:
                binance: zip
                kraken: json.compressed
                okx: zip
            trades: h5
            raw_price_level_book: json
            compressed_price_level_book: json.compressed
            price_level_book: h5

            # learn
            backtest: h5
            tactic_tuning: h5
            score_evaluation: h5
            scores: h5
            model: joblib

            # oppfile
            oppfile_triggers: h5
            oppfile_signal: h5
            oppfile_enhanced: h5
            oppfile_header: h5
            oppfile_price_level_book: h5
        """
    )


def test_storage_from_yaml(storage_config_yaml):
    assert StorageConfig.from_yaml(storage_config_yaml) == StorageConfig(
        path_format={
            PathFormatType.RAW_DATA: "data/raw_data/{version}/{exchange}/{asset_type}/{trading_pair}/{data_segment}/{date}.{extension}",
            PathFormatType.OPPFILE: "data/learn/{version}/dataset/{basket}/{data_segment}/{date}.{extension}",
            PathFormatType.LEARN: "data/learn/{version}/{rolling_learn_id}/{learn_id}/{basket}/{data_segment}/{date}.{extension}",
        },
        extension={
            DataSegment.RAW_TRADES: {
                ExchangeType.BINANCE: "zip",
                ExchangeType.KRAKEN: "json.compressed",
                ExchangeType.OKX: "zip",
            },
            DataSegment.TRADES: "h5",
            DataSegment.RAW_PRICE_LEVEL_BOOK: "json",
            DataSegment.COMPRESSED_PRICE_LEVEL_BOOK: "json.compressed",
            DataSegment.PRICE_LEVEL_BOOK: "h5",
            DataSegment.BACKTEST: "h5",
            DataSegment.TACTIC_TUNING: "h5",
            DataSegment.SCORE_EVALUATION: "h5",
            DataSegment.SCORES: "h5",
            DataSegment.MODEL: "joblib",
            DataSegment.OPPFILE_TRIGGERS: "h5",
            DataSegment.OPPFILE_SIGNAL: "h5",
            DataSegment.OPPFILE_ENHANCED: "h5",
            DataSegment.OPPFILE_HEADER: "h5",
            DataSegment.OPPFILE_PRICE_LEVEL_BOOK: "h5",
        },
    )
