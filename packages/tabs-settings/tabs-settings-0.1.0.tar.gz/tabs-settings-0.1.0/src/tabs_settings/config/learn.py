from __future__ import annotations

from dataclasses import dataclass

from tabs_settings.config.backtest import BacktestConfig
from tabs_settings.config.basket import Basket
from tabs_settings.config.fee import Fee
from tabs_settings.config.fit import FitConfig
from tabs_settings.config.oppfile import OppfileConfig
from tabs_settings.config.partition import Partition
from tabs_settings.config.stochastic_optimization import StochasticOptimizationConfig


@dataclass(frozen=True)
class LearnConfig:
    basket: Basket
    partition: Partition
    fit: FitConfig
    score_evaluation: StochasticOptimizationConfig
    tactic_tuning: StochasticOptimizationConfig
    backtest: BacktestConfig
    oppfile: OppfileConfig
    fee: Fee
    roll_name: str

    @classmethod
    def from_yaml(cls, settings: dict) -> LearnConfig:
        basket = Basket.from_yaml(settings["basket"])
        partition = Partition.from_yaml(settings["partition"])
        fit = FitConfig.from_yaml(settings["fit"])
        score_evaluation = StochasticOptimizationConfig.from_yaml(
            settings["score_evaluation"]
        )
        tactic_tuning = StochasticOptimizationConfig.from_yaml(
            settings["tactic_tuning"]
        )
        backtest = BacktestConfig.from_yaml(settings["backtest"])
        oppfile = OppfileConfig.from_yaml(settings["oppfile"])
        fee = Fee.from_yaml(settings["fees"])
        roll_name = settings["roll_name"]
        return cls(
            basket,
            partition,
            fit,
            score_evaluation,
            tactic_tuning,
            backtest,
            oppfile,
            fee,
            roll_name,
        )

    def __post_init__(self) -> None:
        self._settings_check()

    def _settings_check(self) -> None:
        # check that the horizons used during the learn
        # (in particular for fitting and scoring)
        # are a subset of the horizons computed in the oppfile
        used_horizons = set(self.fit.horizons)
        if "horizons" in self.score_evaluation.dimensions:
            used_horizons = used_horizons | set(
                self.score_evaluation.dimensions["horizons"]
            )

        oppfile_horizons = self.oppfile.horizons

        if not used_horizons.issubset(oppfile_horizons):
            raise ValueError(
                f"Horizons used in the learn ({used_horizons}) are not a subset of the"
                f" horizons computed in the oppfile ({oppfile_horizons})."
            )

        # check that the fees computed in the oppfile are a subset of the fees used
        # in the learn
        oppfile_fees = set(self.oppfile.fees)
        used_fees = set(self.score_evaluation.dimensions["fee"])
        if not used_fees.issubset(oppfile_fees):
            raise ValueError(
                f"Fees computed in the oppfile ({oppfile_fees}) are not a subset of the"
                f" fees used in the learn ({used_fees})."
            )

    @property
    def as_yaml(self) -> dict:
        return {
            "basket": self.basket.as_yaml,
            "partition": self.partition.as_yaml,
            "fit": self.fit.as_yaml,
            "score_evaluation": self.score_evaluation.as_yaml,
            "tactic_tuning": self.tactic_tuning.as_yaml,
            "backtest": self.backtest.as_yaml,
            "oppfile": self.oppfile.as_yaml,
            "fees": self.fee.as_yaml,
            "roll_name": self.roll_name,
        }

    @property
    def name(self) -> str:
        return f"{self.roll_name}/{self.basket.name}-{self.partition.name}"

    @property
    def all_dates(self) -> tuple[str, ...]:
        return self.partition.all_dates
