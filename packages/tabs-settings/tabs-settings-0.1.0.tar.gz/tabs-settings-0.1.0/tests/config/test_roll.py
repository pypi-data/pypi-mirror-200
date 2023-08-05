import pytest

from tabs_settings.config.partition import Partition
from tabs_settings.config.roll import Roll

SEED = 0


@pytest.mark.parametrize(
    "roll_settings, expected",
    [
        (
            {
                "date_to": "20210105",
                "n_dates": 5,
                "n_days_fit": 1,
                "n_days_score_evaluation": 1,
                "n_days_tactic_tuning": 1,
                "n_days_test": 1,
                "seed": SEED,
            },
            Roll(
                partitions=(
                    Partition(
                        fit_dates=frozenset({"20210104"}),
                        score_evaluation_dates=frozenset({"20210103"}),
                        tactic_tuning_dates=frozenset({"20210102"}),
                        test_dates=frozenset({"20210101"}),
                        seed=0,
                    ),
                    Partition(
                        fit_dates=frozenset({"20210105"}),
                        score_evaluation_dates=frozenset({"20210104"}),
                        tactic_tuning_dates=frozenset({"20210103"}),
                        test_dates=frozenset({"20210102"}),
                        seed=0,
                    ),
                )
            ),
        ),
    ],
)
def test_roll_from_yaml(roll_settings, expected):
    assert Roll.from_yaml(roll_settings) == expected


@pytest.mark.parametrize(
    "date_to, n_dates, n_days_fit, n_days_score_evaluation, n_days_tactic_tuning,"
    " n_days_test, expected_output",
    [
        (
            "20220105",
            5,
            1,
            1,
            1,
            1,
            (
                Partition(
                    fit_dates=frozenset({"20220104"}),
                    score_evaluation_dates=frozenset({"20220103"}),
                    tactic_tuning_dates=frozenset({"20220102"}),
                    test_dates=frozenset({"20220101"}),
                    seed=0,
                ),
                Partition(
                    fit_dates=frozenset({"20220105"}),
                    score_evaluation_dates=frozenset({"20220104"}),
                    tactic_tuning_dates=frozenset({"20220103"}),
                    test_dates=frozenset({"20220102"}),
                    seed=0,
                ),
            ),
        ),
        (
            "20220103",
            3,
            1,
            1,
            1,
            1,
            (),
        ),
        (
            "20220106",
            8,
            1,
            1,
            1,
            2,
            (
                Partition(
                    fit_dates=frozenset({"20220104"}),
                    score_evaluation_dates=frozenset({"20220103"}),
                    tactic_tuning_dates=frozenset({"20220102"}),
                    test_dates=frozenset({"20220101", "20211231"}),
                    seed=0,
                ),
                Partition(
                    fit_dates=frozenset({"20220106"}),
                    score_evaluation_dates=frozenset({"20220105"}),
                    tactic_tuning_dates=frozenset({"20220104"}),
                    test_dates=frozenset({"20220102", "20220103"}),
                    seed=0,
                ),
            ),
        ),
    ],
)
def test_roll_from_parameters(
    date_to,
    n_dates,
    n_days_fit,
    n_days_score_evaluation,
    n_days_tactic_tuning,
    n_days_test,
    expected_output,
):
    roll = Roll.from_parameters(
        date_to,
        n_dates,
        n_days_fit,
        n_days_score_evaluation,
        n_days_tactic_tuning,
        n_days_test,
        SEED,
    )
    assert roll.partitions == expected_output


def test_roll_as_yaml():
    yaml = {
        "date_to": "20220106",
        "n_dates": 5,
        "n_days_fit": 1,
        "n_days_score_evaluation": 1,
        "n_days_tactic_tuning": 1,
        "n_days_test": 1,
        "seed": SEED,
    }
    roll = Roll.from_yaml(yaml)
    assert roll.as_yaml == yaml


@pytest.mark.parametrize(
    "roll_settings",
    [
        (
            {
                "date_to": "20220106",
                "n_dates": 5,
                "n_days_fit": 1,
                "n_days_score_evaluation": 1,
                "n_days_tactic_tuning": 1,
                "n_days_test": 1,
                "seed": SEED,
            }
        ),
        (
            {
                "date_to": "20220106",
                "n_dates": 150,
                "n_days_fit": 20,
                "n_days_score_evaluation": 10,
                "n_days_tactic_tuning": 10,
                "n_days_test": 5,
                "seed": SEED,
            }
        ),
    ],
)
def test_roll_yaml_round_trip(roll_settings):
    roll = Roll.from_yaml(roll_settings)
    assert roll.as_yaml == roll_settings


@pytest.mark.parametrize(
    "roll_settings, expected",
    [
        (
            {
                "date_to": "20210107",
                "n_dates": 6,
                "n_days_fit": 1,
                "n_days_score_evaluation": 1,
                "n_days_tactic_tuning": 1,
                "n_days_test": 1,
            },
            ("20210102", "20210103", "20210104", "20210105", "20210106", "20210107"),
        )
    ],
)
def test_all_dates(roll_settings, expected):
    assert Roll.from_parameters(**roll_settings).all_dates == expected


@pytest.mark.parametrize(
    "roll_settings, expected",
    [
        (
            {
                "date_to": "20210107",
                "n_dates": 6,
                "n_days_fit": 1,
                "n_days_score_evaluation": 1,
                "n_days_tactic_tuning": 1,
                "n_days_test": 1,
                "seed": 1,
            },
            "20210107_6",
        ),
    ],
)
def test_roll_name(roll_settings, expected):
    assert Roll.from_yaml(roll_settings).name == expected
