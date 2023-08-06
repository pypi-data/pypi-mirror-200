from tabs_settings.config.action_type import ActionType


def test_valid_actions():
    valid_actions = ActionType.valid_actions()
    assert len(valid_actions) == 3
    assert ActionType.BUY in valid_actions
    assert ActionType.SELL in valid_actions
    assert ActionType.NEUTRAL in valid_actions


def test_impact_actions():
    impact_actions = ActionType.impact_actions()
    assert len(impact_actions) == 2
    assert ActionType.BUY in impact_actions
    assert ActionType.SELL in impact_actions


def test_enum_values():
    assert ActionType.SELL.value == "sell"
    assert ActionType.NEUTRAL.value == "neutral"
    assert ActionType.BUY.value == "buy"
    assert ActionType.INVALID.value == "invalid"
