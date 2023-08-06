from __future__ import annotations

from dataclasses import dataclass

from tabs_settings.config.horizon import Horizon


@dataclass(frozen=True)
class FitConfig:
    model_params: dict
    pca_params: dict
    horizons: tuple[Horizon]

    @classmethod
    def from_yaml(cls, settings: dict) -> FitConfig:
        """
        model_params:
            penalty: 'l2'
            dual: False
            tol: 0.0001
            C: 10.0
            fit_intercept: True
            intercept_scaling: 1
            class_weight:
            random_state: 0
            solver: 'newton-cholesky'
            max_iter: 100
            multi_class: 'auto'
            verbose: 0
            warm_start: False
            n_jobs: -1
            l1_ratio:
        horizons:
            - 100ms
            - 1s
        pca_params:
            n_components: 0.001
        """
        return cls(
            model_params=settings["model_params"],
            pca_params=settings["pca_params"],
            horizons=tuple(Horizon.from_yaml(v) for v in settings["horizons"]),
        )

    @property
    def as_yaml(self) -> dict:
        return {
            "model_params": self.model_params,
            "pca_params": self.pca_params,
            "horizons": [v.as_yaml for v in self.horizons],
        }
