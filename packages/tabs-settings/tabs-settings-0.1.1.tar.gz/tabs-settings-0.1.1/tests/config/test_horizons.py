import pytest

from tabs_settings.config.horizon import Horizon


def test_horizon_from_yaml():
    horizon = Horizon.from_yaml("100ms")
    assert horizon.name == "100ms"


def test_horizon_as_yaml():
    horizon = Horizon.from_yaml("100ms")
    assert horizon.as_yaml == "100ms"


@pytest.mark.parametrize(
    "horizon1, horizon2, expected",
    [
        ("100ms", "100ms", False),
        ("100ms", "1s", True),
        ("1s", "100ms", False),
        ("1s", "1s", False),
        ("1s", "2s", True),
        ("2s", "1s", False),
        ("1m", "1s", False),
        ("1m", "1m", False),
        ("1m", "2m", True),
        ("2m", "1m", False),
        ("1h", "1m", False),
        ("1h", "1h", False),
        ("1h", "2h", True),
        ("2h", "1h", False),
    ],
)
def test_horizon_lt(horizon1, horizon2, expected):
    if expected:
        assert Horizon.from_yaml(horizon1) < Horizon.from_yaml(horizon2)
    else:
        assert not Horizon.from_yaml(horizon1) < Horizon.from_yaml(horizon2)


@pytest.mark.parametrize(
    "horizon, expected",
    [
        ("100ms", 100 * 10**6),
        ("1s", 10**9),
        ("1m", 60 * 10**9),
        ("2m", 2 * 60 * 10**9),
        ("1h", 60 * 60 * 10**9),
    ],
)
def test_as_nanoseconds(horizon, expected):
    result = Horizon.from_yaml(horizon).as_nanoseconds
    assert result == expected


@pytest.mark.parametrize(
    "horizon, expected_value, expected_unit",
    [
        ("100ms", 100, "ms"),
        ("1s", 1, "s"),
        ("1m", 1, "m"),
        ("2m", 2, "m"),
        ("1h", 1, "h"),
    ],
)
def test_value_and_unit(horizon, expected_value, expected_unit):
    result = Horizon.from_yaml(horizon)._value_and_unit
    assert result == (expected_value, expected_unit)
