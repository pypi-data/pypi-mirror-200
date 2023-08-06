from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum, auto
from typing import Optional

import numpy as np


class PartitionType(Enum):
    FIT = auto()
    SCORE_EVALUATION = auto()
    TACTIC_TUNING = auto()
    TEST = auto()


@dataclass(frozen=True)
class Partition:
    fit_dates: frozenset[str]
    score_evaluation_dates: frozenset[str]
    tactic_tuning_dates: frozenset[str]
    test_dates: frozenset[str]
    seed: int

    def __lt__(self, other: Partition) -> bool:
        return self.partition_date < other.partition_date

    @classmethod
    def from_yaml(cls, settings: dict) -> Partition:
        return cls.from_parameters(
            settings["date_from"],
            settings["n_days_fit"],
            settings["n_days_score_evaluation"],
            settings["n_days_tactic_tuning"],
            settings["n_days_test"],
            settings["seed"],
        )

    @classmethod
    def from_parameters(
        cls,
        date_from: date | str | int,
        n_days_fit: int,
        n_days_score_evaluation: int,
        n_days_tactic_tuning: int,
        n_days_test: int,
        seed: int,
    ) -> Partition:
        """
        fit, score eval and tactic tuning are shuffled
        test is contiguous in time, and is the last n_days_test days
        """
        if isinstance(date_from, int):
            date_from = str(date_from)
        if isinstance(date_from, str):
            date_from = date.fromisoformat(date_from)
        assert isinstance(date_from, date)

        roll_size = (
            n_days_fit + n_days_score_evaluation + n_days_tactic_tuning + n_days_test
        )
        roll_dates = [date_from + timedelta(days=i) for i in range(roll_size)]
        roll_dates = [roll_date.strftime("%Y%m%d") for roll_date in roll_dates]

        # the test dates must be contiguous in time
        test_dates = roll_dates[:n_days_test]
        remaining_dates = roll_dates[n_days_test:]

        # set the seed so that the partition is the same for all backfillple projects
        np.random.seed(seed)

        dates_shuffled = np.random.permutation(remaining_dates)
        fit_dates = dates_shuffled[:n_days_fit]
        score_evaluation_dates = dates_shuffled[
            n_days_fit : n_days_fit + n_days_score_evaluation
        ]
        tactic_tuning_dates = dates_shuffled[n_days_fit + n_days_score_evaluation :]

        return Partition(
            frozenset(fit_dates),
            frozenset(score_evaluation_dates),
            frozenset(tactic_tuning_dates),
            frozenset(test_dates),
            seed,
        )

    @property
    def as_yaml(self) -> dict:
        return {
            "date_from": self.partition_date,
            "n_days_fit": len(self.fit_dates),
            "n_days_score_evaluation": len(self.score_evaluation_dates),
            "n_days_tactic_tuning": len(self.tactic_tuning_dates),
            "n_days_test": len(self.test_dates),
            "seed": self.seed,
        }

    @classmethod
    def from_expanded_yaml(cls, settings: dict) -> Partition:
        return cls(**settings)

    @property
    def as_expanded_yaml(self) -> dict[str, tuple[str]]:
        return {
            "fit_dates": tuple(sorted(self.fit_dates)),
            "score_evaluation_dates": tuple(sorted(self.score_evaluation_dates)),
            "tactic_tuning_dates": tuple(sorted(self.tactic_tuning_dates)),
            "test_dates": tuple(sorted(self.test_dates)),
        }

    @property
    def n_dates(self) -> int:
        return len(self.get_partition())

    @property
    def n_fit_dates(self) -> int:
        return len(self.fit_dates)

    @property
    def n_score_evaluation_dates(self) -> int:
        return len(self.score_evaluation_dates)

    @property
    def n_tactic_tuning_dates(self) -> int:
        return len(self.tactic_tuning_dates)

    @property
    def n_test_dates(self) -> int:
        return len(self.test_dates)

    @property
    def name(self) -> str:
        return f"{self.partition_date}_{self.n_dates}"

    @property
    def partition_date(self) -> str:
        return sorted(self.get_partition())[0]

    @property
    def all_dates(self) -> tuple[str]:
        return tuple(sorted(self.get_partition()))

    def get_partition(
        self, partition_type: Optional[PartitionType] = None
    ) -> frozenset[str]:
        if partition_type is PartitionType.FIT:
            return self.fit_dates
        elif partition_type is PartitionType.SCORE_EVALUATION:
            return self.score_evaluation_dates
        elif partition_type is PartitionType.TACTIC_TUNING:
            return self.tactic_tuning_dates
        elif partition_type is PartitionType.TEST:
            return self.test_dates
        elif partition_type is None:
            return (
                self.fit_dates
                | self.score_evaluation_dates
                | self.tactic_tuning_dates
                | self.test_dates
            )

    def get_complementary_partition(
        self, partition_type: PartitionType
    ) -> frozenset[str]:
        all_dates = self.get_partition()
        dates_excluded = self.get_partition(partition_type)
        dates = all_dates - dates_excluded
        return dates
