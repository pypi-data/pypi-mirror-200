import pytest
from skopt import Space
from skopt.space import Real

from tabs_settings.config.search_space import SearchSpace


@pytest.mark.parametrize(
    "bounds_settings, expected_vars, expected_space",
    [
        (
            {
                "sided": {
                    "variable_1": {"low": 0, "high": 10},
                    "variable_2": {"low": -5, "high": 5},
                }
            },
            ("variable_1_BUY", "variable_1_SELL", "variable_2_BUY", "variable_2_SELL"),
            Space(
                [
                    Real(low=0, high=10),
                    Real(low=0, high=10),
                    Real(low=-5, high=5),
                    Real(low=-5, high=5),
                ]
            ),
        ),
        (
            {
                "sided": {
                    "variable_1": {"low": 0, "high": 10},
                    "variable_2": {"low": -5, "high": 5},
                },
                "not_sided": {"variable_3": {"low": 0, "high": 100}},
            },
            (
                "variable_1_BUY",
                "variable_1_SELL",
                "variable_2_BUY",
                "variable_2_SELL",
                "variable_3",
            ),
            Space(
                [
                    Real(low=0, high=10),
                    Real(low=0, high=10),
                    Real(low=-5, high=5),
                    Real(low=-5, high=5),
                    Real(low=0, high=100),
                ]
            ),
        ),
        (
            {"not_sided": {"variable_3": {"low": 0, "high": 100}}},
            ("variable_3",),
            Space([Real(low=0, high=100)]),
        ),
        ({}, (), Space([])),
    ],
)
def test_search_space_from_yaml(bounds_settings, expected_vars, expected_space):
    search_space = SearchSpace.from_yaml(bounds_settings)
    assert search_space.variables_name == expected_vars
    assert search_space.space == expected_space


@pytest.mark.parametrize(
    "settings",
    [
        (
            {
                "sided": {
                    "opening_threshold": {
                        "low": 0.0001,
                        "high": 0.1,
                        "prior": "uniform",
                        "base": 10,
                    }
                },
                "not_sided": {
                    "max_order_size": {
                        "low": 11,
                        "high": 11.01,
                        "prior": "uniform",
                        "base": 10,
                    }
                },
            }
        ),
        (
            {
                "sided": {
                    "opening_threshold": {
                        "low": 0.0001,
                        "high": 0.1,
                        "prior": "uniform",
                        "base": 10,
                    }
                }
            }
        ),
    ],
)
def test_search_space_as_yaml(settings):
    search_space = SearchSpace.from_yaml(settings)
    assert search_space.as_yaml == settings
