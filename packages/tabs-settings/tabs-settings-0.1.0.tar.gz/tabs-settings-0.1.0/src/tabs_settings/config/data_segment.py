from __future__ import annotations

from enum import Enum


class DataSegment(Enum):
    # raw market data
    RAW_TRADES = "raw_trades"
    TRADES = "trades"
    RAW_PRICE_LEVEL_BOOK = "raw_price_level_book"
    COMPRESSED_PRICE_LEVEL_BOOK = "compressed_price_level_book"
    PRICE_LEVEL_BOOK = "price_level_book"

    # oppfiles
    OPPFILE_TRIGGERS = "oppfile_triggers"
    OPPFILE_HEADER = "oppfile_header"
    OPPFILE_SIGNAL = "oppfile_signal"
    OPPFILE_PRICE_LEVEL_BOOK = "oppfile_price_level_book"
    OPPFILE_ENHANCED = "oppfile_enhanced"

    # tabs
    MODEL = "model"
    SCORES = "scores"
    SCORE_EVALUATION = "score_evaluation"
    TACTIC_TUNING = "tactic_tuning"
    BACKTEST = "backtest"

    # function that returns the list of market data data segments
    @staticmethod
    def get_market_data_data_segments() -> frozenset[DataSegment]:
        return frozenset(
            {
                DataSegment.RAW_TRADES,
                DataSegment.TRADES,
                DataSegment.RAW_PRICE_LEVEL_BOOK,
                DataSegment.COMPRESSED_PRICE_LEVEL_BOOK,
                DataSegment.PRICE_LEVEL_BOOK,
            }
        )

    # function that returns the list of oppfile data segments
    @staticmethod
    def get_oppfile_data_segments() -> frozenset[DataSegment]:
        return frozenset(
            {
                DataSegment.OPPFILE_TRIGGERS,
                DataSegment.OPPFILE_SIGNAL,
                DataSegment.OPPFILE_PRICE_LEVEL_BOOK,
                DataSegment.OPPFILE_ENHANCED,
                DataSegment.OPPFILE_HEADER,
            }
        )

    # function that returns the list of learn data segments
    @staticmethod
    def get_learn_data_segments() -> frozenset[DataSegment]:
        return frozenset(
            {
                DataSegment.MODEL,
                DataSegment.SCORES,
                DataSegment.SCORE_EVALUTATION,
                DataSegment.TACTIC_TUNING,
                DataSegment.BACKTEST,
            }
        )

    @property
    def is_oppfile(self) -> bool:
        return self in DataSegment.get_oppfile_data_segments()

    @property
    def is_market_data(self) -> bool:
        return self in DataSegment.get_market_data_data_segments()
