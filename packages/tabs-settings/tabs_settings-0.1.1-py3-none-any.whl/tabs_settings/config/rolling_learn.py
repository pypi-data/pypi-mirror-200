from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from tabs_settings.config.basket import Basket
from tabs_settings.config.learn import LearnConfig
from tabs_settings.config.roll import Roll


@dataclass(frozen=True)
class RollingLearnConfig:
    roll: Roll
    learns: tuple[LearnConfig, ...]

    # implement iterate method to iterate over learns
    def __iter__(self):
        return iter(self.learns)

    def __next__(self):
        return self.__next__()

    def __getitem__(self, item: int) -> LearnConfig:
        if isinstance(item, int):
            return self.learns[item]

    def __len__(self):
        return len(self.learns)

    @classmethod
    def from_yaml(cls, settings: dict) -> RollingLearnConfig:
        learns = []
        roll = Roll.from_yaml(settings["roll"])
        for partition in roll:
            learn_settings = deepcopy(settings)
            del learn_settings["roll"]
            learn_settings["partition"] = partition.as_yaml
            learn_settings["roll_name"] = roll.name
            learn = LearnConfig.from_yaml(learn_settings)
            learns.append(learn)
        return RollingLearnConfig(roll, tuple(learns))

    @property
    def as_yaml(self) -> dict:
        learn_yaml = deepcopy((self.learns[0].as_yaml))
        # replace partition with roll
        learn_yaml["roll"] = self.roll.as_yaml
        del learn_yaml["partition"]
        del learn_yaml["roll_name"]
        return learn_yaml

    @property
    def basket(self) -> Basket:
        return self.learns[0].basket

    @property
    def all_dates(self) -> tuple[str, ...]:
        return self.roll.all_dates

    # @property
    # def name(self) -> str:
    #     return f"{self.basket.name}-{self.roll.name}"
