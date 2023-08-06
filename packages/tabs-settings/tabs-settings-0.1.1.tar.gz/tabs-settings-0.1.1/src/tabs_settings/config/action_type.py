from __future__ import annotations

from enum import Enum


class ActionType(Enum):
    SELL = "sell"
    NEUTRAL = "neutral"
    BUY = "buy"
    INVALID = "invalid"

    @staticmethod
    def valid_actions() -> tuple[ActionType, ...]:
        return (ActionType.BUY, ActionType.SELL, ActionType.NEUTRAL)

    @staticmethod
    def impact_actions() -> tuple[ActionType, ActionType]:
        return (ActionType.BUY, ActionType.SELL)
