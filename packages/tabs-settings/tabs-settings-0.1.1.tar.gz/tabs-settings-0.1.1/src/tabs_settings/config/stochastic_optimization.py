from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from tabs_settings.config.horizon import Horizon
from tabs_settings.config.search_space import SearchSpace


@dataclass(frozen=True)
class StochasticOptimizationConfig:
    objective: dict
    dimensions: dict
    n_iterations: int
    optimizer_settings: dict
    search_space: SearchSpace

    @classmethod
    def from_yaml(cls, settings: dict) -> StochasticOptimizationConfig:
        """
        objctive:
        dimensions:
            horizons:
                - 1m
                - 5m
                - 10m
            fee:
                - 0 # nofee
        n_iterations: 110
        optimizer_settings:
            base_estimator: gp # or dummy but does not work as good
            n_initial_points: 100
            initial_point_generator: random
            acq_func: gp_hedge
            acq_optimizer: lbfgs
            random_state: 0
            model_queue_size:
            acq_func_kwargs:
                n_restarts_optimizer: 1
        search_space:
            sided:
                quantile:
                    low: 0.00001
                    high: 0.1
                    prior: log-uniform
                    base: 10
        """
        settings = deepcopy(settings)
        dimensions = settings["dimensions"]
        if dimensions is not None:
            for key, value in dimensions.items():
                if key == "horizons":
                    dimensions[key] = [Horizon.from_yaml(v) for v in value]

        return cls(
            objective=settings["objective"],
            dimensions=settings["dimensions"],
            n_iterations=settings["n_iterations"],
            optimizer_settings=settings["optimizer_settings"],
            search_space=SearchSpace.from_yaml(settings["search_space"]),
        )

    @property
    def as_yaml(self) -> dict:
        dimensions_yaml = deepcopy(self.dimensions)
        if dimensions_yaml is not None:
            for key, value in dimensions_yaml.items():
                if key == "horizons":
                    dimensions_yaml[key] = [v.as_yaml for v in value]
        return {
            "objective": self.objective,
            "dimensions": dimensions_yaml,
            "n_iterations": self.n_iterations,
            "optimizer_settings": self.optimizer_settings,
            "search_space": self.search_space.as_yaml,
        }
