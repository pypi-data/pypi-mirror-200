from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from functools import reduce
from operator import or_

import pandas as pd

from tabs_settings.config.partition import Partition


@dataclass(frozen=True)
class Roll:
    partitions: tuple[Partition, ...]

    def __iter__(self):
        return self.partitions.__iter__()

    def __next__(self):
        return self.__next__()

    def __getitem__(self, item: int | str) -> Partition:
        if isinstance(item, int):
            return self.partitions[item]
        elif isinstance(item, str):
            return [
                partition
                for partition in self.partitions
                if partition.partition_date == item
            ][0]

    @classmethod
    def from_yaml(cls, settings: dict) -> Roll:
        """
        date_to: 20201231
        n_dates: 100
        n_days_fit: 30
        n_days_score_evaluation: 30
        n_days_tactic_tuning: 30
        n_days_test: 30
        seed: 1
        """
        return cls.from_parameters(**settings)

    @classmethod
    def from_parameters(
        cls,
        date_to: str,
        n_dates: int,
        n_days_fit: int,
        n_days_score_evaluation: int,
        n_days_tactic_tuning: int,
        n_days_test: int,
        seed: int = 1,
    ) -> Roll:
        """
        python convention is used:
        - date_to is included
        """
        date_to_obj = pd.to_datetime(date_to, format="%Y%m%d") + timedelta(days=1)
        date_from_obj = date_to_obj - pd.Timedelta(days=n_dates)

        n_train_dates = n_days_fit + n_days_score_evaluation + n_days_tactic_tuning
        n_effective_test_dates = (date_to_obj - date_from_obj).days - n_train_dates
        n_partitions = n_effective_test_dates // n_days_test

        partitions = []
        for i in range(n_partitions):
            roll_end_date = date_to_obj - pd.Timedelta(days=n_days_test * i)
            roll_start_date = roll_end_date - pd.Timedelta(
                days=n_train_dates + n_days_test
            )
            partition = Partition.from_parameters(
                roll_start_date,
                n_days_fit,
                n_days_score_evaluation,
                n_days_tactic_tuning,
                n_days_test,
                seed,
            )
            partitions.append(partition)
        return cls(tuple(sorted(partitions)))

    @property
    def as_yaml(self) -> dict:
        yaml = self.partitions[0].as_yaml
        del yaml["date_from"]
        yaml["date_to"] = self.last_date
        yaml["n_dates"] = self.n_dates
        return yaml

    @property
    def all_dates(self) -> tuple[str, ...]:
        all_dates = reduce(
            or_,
            [set(partition.all_dates) for partition in self.partitions],
            frozenset(),
        )
        return tuple(sorted(all_dates))

    @property
    def last_date(self) -> str:
        return max(self.all_dates)

    @property
    def first_date(self) -> str:
        return min(self.all_dates)

    @property
    def n_dates(self):
        return len(self.all_dates)

    @property
    def name(self) -> str:
        return f"{self.last_date}_{self.n_dates}"
