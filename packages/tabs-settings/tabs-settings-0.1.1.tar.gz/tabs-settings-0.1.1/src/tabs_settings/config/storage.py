from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.exchange_type import ExchangeType


class PathFormatType(Enum):
    RAW_DATA = "raw_data"
    OPPFILE = "oppfile"
    LEARN = "learn"


@dataclass(frozen=True)
class StorageConfig:
    path_format: dict
    extension: dict

    @classmethod
    def from_yaml(cls, settings: dict) -> StorageConfig:
        """
        format:
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
            scores_evaluation: h5
            scores: h5
            model: h5
            oppfile: h5
        """
        # interpret elements of extension
        extension = {}
        for data_segment, exchange_extension in settings["extension"].items():
            if isinstance(exchange_extension, dict):
                extension[DataSegment(data_segment)] = {
                    ExchangeType.from_settings(exchange): extension
                    for exchange, extension in exchange_extension.items()
                }
            else:
                extension[DataSegment(data_segment)] = exchange_extension

        # interpret elements of format
        path_format = {}
        for format_type, format_name in settings["path_format"].items():
            path_format[PathFormatType(format_type)] = format_name

        return cls(path_format, extension)
