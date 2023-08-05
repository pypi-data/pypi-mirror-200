from datetime import date

import pytest

from tabs_settings.config.partition import Partition, PartitionType

SEED = 0


@pytest.mark.parametrize(
    "settings, expected",
    [
        (
            {
                "date_from": "20200101",
                "n_days_fit": 5,
                "n_days_score_evaluation": 3,
                "n_days_tactic_tuning": 2,
                "n_days_test": 1,
                "seed": SEED,
            },
            Partition(
                fit_dates=frozenset(
                    {"20200103", "20200104", "20200106", "20200110", "20200111"}
                ),
                score_evaluation_dates=frozenset({"20200105", "20200108", "20200109"}),
                tactic_tuning_dates=frozenset({"20200102", "20200107"}),
                test_dates=frozenset({"20200101"}),
                seed=SEED,
            ),
        ),
    ],
)
def test_partition_from_yaml(settings, expected):
    assert Partition.from_yaml(settings) == expected


@pytest.mark.parametrize(
    "partition, expected",
    [
        (
            Partition(
                fit_dates=frozenset({"20200101", "20200102", "20200103"}),
                score_evaluation_dates=frozenset({"20200104", "20200105"}),
                tactic_tuning_dates=frozenset({"20200106", "20200107"}),
                test_dates=frozenset({"20200108", "20200109"}),
                seed=SEED,
            ),
            {
                "date_from": "20200101",
                "n_days_fit": 3,
                "n_days_score_evaluation": 2,
                "n_days_tactic_tuning": 2,
                "n_days_test": 2,
                "seed": SEED,
            },
        ),
    ],
)
def test_partition_as_yaml(partition, expected):
    assert partition.as_yaml == expected


def test_partition_yaml_round_trip():
    settings = {
        "date_from": "20200101",
        "n_days_fit": 5,
        "n_days_score_evaluation": 3,
        "n_days_tactic_tuning": 2,
        "n_days_test": 1,
        "seed": SEED,
    }
    partition = Partition.from_yaml(settings)
    assert partition.as_yaml == settings


@pytest.mark.parametrize(
    "partition, expected",
    [
        (
            Partition(
                fit_dates=frozenset({"20200101", "20200102", "20200103"}),
                score_evaluation_dates=frozenset({"20200104", "20200105"}),
                tactic_tuning_dates=frozenset({"20200106", "20200107"}),
                test_dates=frozenset({"20200108", "20200109"}),
                seed=SEED,
            ),
            {
                "fit_dates": ("20200101", "20200102", "20200103"),
                "score_evaluation_dates": ("20200104", "20200105"),
                "tactic_tuning_dates": ("20200106", "20200107"),
                "test_dates": ("20200108", "20200109"),
            },
        ),
    ],
)
def test_partition_as_expanded_yaml(partition, expected):
    assert partition.as_expanded_yaml == expected


@pytest.mark.parametrize(
    "date_from, n_days_fit, n_days_score_evaluation, n_days_tactic_tuning,"
    " n_days_test, expected_output",
    [
        (
            date(2022, 1, 1),
            5,
            3,
            2,
            1,
            Partition(
                fit_dates=frozenset(
                    {"20220103", "20220104", "20220106", "20220110", "20220111"}
                ),
                score_evaluation_dates=frozenset({"20220105", "20220108", "20220109"}),
                tactic_tuning_dates=frozenset({"20220102", "20220107"}),
                test_dates=frozenset({"20220101"}),
                seed=SEED,
            ),
        ),
        (
            date(2022, 1, 1),
            5,
            3,
            2,
            2,
            Partition(
                fit_dates=frozenset(
                    {"20220111", "20220107", "20220105", "20220112", "20220104"}
                ),
                score_evaluation_dates=frozenset({"20220110", "20220106", "20220109"}),
                tactic_tuning_dates=frozenset({"20220103", "20220108"}),
                test_dates=frozenset({"20220102", "20220101"}),
                seed=SEED,
            ),
        ),
    ],
)
def test_get_partition(
    date_from,
    n_days_fit,
    n_days_score_evaluation,
    n_days_tactic_tuning,
    n_days_test,
    expected_output,
):
    partition = Partition.from_parameters(
        date_from,
        n_days_fit,
        n_days_score_evaluation,
        n_days_tactic_tuning,
        n_days_test,
        SEED,
    )
    assert partition == expected_output


@pytest.mark.parametrize(
    "date_from, n_days_fit, n_days_score_evaluation, n_days_tactic_tuning,"
    " n_days_test, expected_model_date",
    [
        (date(2022, 1, 1), 3, 2, 1, 2, "20220101"),
        (date(2022, 1, 2), 1, 2, 3, 2, "20220102"),
        (date(2022, 1, 3), 2, 2, 2, 2, "20220103"),
    ],
)
def test_partition_date(
    date_from,
    n_days_fit,
    n_days_score_evaluation,
    n_days_tactic_tuning,
    n_days_test,
    expected_model_date,
):
    partition = Partition.from_parameters(
        date_from,
        n_days_fit,
        n_days_score_evaluation,
        n_days_tactic_tuning,
        n_days_test,
        SEED,
    )
    assert partition.partition_date == expected_model_date


@pytest.mark.parametrize(
    "date_from, n_days_fit, n_days_score_evaluation, n_days_tactic_tuning,"
    " n_days_test, expected_n_dates",
    [
        (date(2022, 1, 1), 3, 2, 1, 2, 8),
        (date(2022, 1, 1), 1, 2, 3, 2, 8),
        (date(2022, 1, 1), 2, 2, 2, 2, 8),
    ],
)
def test_n_dates(
    date_from,
    n_days_fit,
    n_days_score_evaluation,
    n_days_tactic_tuning,
    n_days_test,
    expected_n_dates,
):
    partition = Partition.from_parameters(
        date_from,
        n_days_fit,
        n_days_score_evaluation,
        n_days_tactic_tuning,
        n_days_test,
        SEED,
    )
    assert partition.n_dates == expected_n_dates


@pytest.mark.parametrize(
    "partition_type, expected_dates",
    [
        (
            PartitionType.FIT,
            frozenset(
                {"20200104", "20200105", "20200106", "20200107", "20200108", "20200109"}
            ),
        ),
        (
            PartitionType.SCORE_EVALUATION,
            frozenset(
                {
                    "20200101",
                    "20200102",
                    "20200103",
                    "20200106",
                    "20200107",
                    "20200108",
                    "20200109",
                }
            ),
        ),
        (
            PartitionType.TACTIC_TUNING,
            frozenset(
                {
                    "20200101",
                    "20200102",
                    "20200103",
                    "20200104",
                    "20200105",
                    "20200108",
                    "20200109",
                }
            ),
        ),
        (
            PartitionType.TEST,
            frozenset(
                {
                    "20200101",
                    "20200102",
                    "20200103",
                    "20200104",
                    "20200105",
                    "20200106",
                    "20200107",
                }
            ),
        ),
    ],
)
def test_get_complementary_partition(partition_type, expected_dates):
    partition = Partition(
        fit_dates=frozenset({"20200101", "20200102", "20200103"}),
        score_evaluation_dates=frozenset({"20200104", "20200105"}),
        tactic_tuning_dates=frozenset({"20200106", "20200107"}),
        test_dates=frozenset({"20200108", "20200109"}),
        seed=SEED,
    )
    assert partition.get_complementary_partition(partition_type) == expected_dates


@pytest.mark.parametrize(
    "partition1, partition2, expected",
    [
        (
            Partition(
                fit_dates=frozenset({"20200101", "20200102", "20200103"}),
                score_evaluation_dates=frozenset({"20200104", "20200105"}),
                tactic_tuning_dates=frozenset({"20200106", "20200107"}),
                test_dates=frozenset({"20200108", "20200109"}),
                seed=SEED,
            ),
            Partition(
                fit_dates=frozenset({"20200111", "20200112", "20200113"}),
                score_evaluation_dates=frozenset({"20200114", "20200115"}),
                tactic_tuning_dates=frozenset({"20200116", "20200117"}),
                test_dates=frozenset({"20200118", "20200119"}),
                seed=SEED,
            ),
            True,
        ),
        (
            Partition(
                fit_dates=frozenset({"20200111", "20200112", "20200113"}),
                score_evaluation_dates=frozenset({"20200114", "20200115"}),
                tactic_tuning_dates=frozenset({"20200116", "20200117"}),
                test_dates=frozenset({"20200118", "20200119"}),
                seed=SEED,
            ),
            Partition(
                fit_dates=frozenset({"20200101", "20200102", "20200103"}),
                score_evaluation_dates=frozenset({"20200104", "20200105"}),
                tactic_tuning_dates=frozenset({"20200106", "20200107"}),
                test_dates=frozenset({"20200108", "20200109"}),
                seed=SEED,
            ),
            False,
        ),
    ],
)
def test_partition_lt(partition1, partition2, expected):
    if expected:
        assert partition1 < partition2
    else:
        assert not (partition1 < partition2)


@pytest.mark.parametrize(
    "partition, expected",
    [
        (
            Partition(
                fit_dates=frozenset({"20200101", "20200102", "20200103"}),
                score_evaluation_dates=frozenset({"20200104", "20200105"}),
                tactic_tuning_dates=frozenset({"20200106", "20200107"}),
                test_dates=frozenset({"20200108", "20200109"}),
                seed=SEED,
            ),
            "20200101_9",
        ),
    ],
)
def test_partition_name(partition, expected):
    assert partition.name == expected


def test_partition_all_dates():
    partition = Partition(
        fit_dates=frozenset({"20200101", "20200102", "20200103"}),
        score_evaluation_dates=frozenset({"20200104", "20200105"}),
        tactic_tuning_dates=frozenset({"20200106", "20200107"}),
        test_dates=frozenset({"20200108", "20200109"}),
        seed=SEED,
    )
    assert partition.all_dates == tuple(
        [
            "20200101",
            "20200102",
            "20200103",
            "20200104",
            "20200105",
            "20200106",
            "20200107",
            "20200108",
            "20200109",
        ]
    )
