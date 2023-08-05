from __future__ import annotations

from dataclasses import dataclass

from skopt import Space
from skopt.space.space import Real

from tabs_settings.config.action_type import ActionType


@dataclass(frozen=True)
class SearchSpace:
    variables_name: tuple[str, ...]
    space: Space

    @classmethod
    def from_yaml(cls, settings: dict) -> SearchSpace:
        """
        sided:
            opening_threshold:
                low: 0.0001
                high: 0.1
                prior: uniform
                base: 10
        not_sided:
            max_order_size:
                low: 11
                high: 11.01
                prior: uniform
                base: 10
        """
        variables_name = []
        dimensions = []
        for section in ("sided", "not_sided"):
            if section in settings:
                for variable_name, description in settings[section].items():
                    if section == "sided":
                        for action in ActionType.impact_actions():
                            v_name = f"{variable_name}_{action.name}"
                            variables_name.append(v_name)
                            dimension = Real(**description)
                            dimensions.append(dimension)
                    else:
                        variables_name.append(variable_name)
                        dimension = Real(**description)
                        dimensions.append(dimension)

        # order variables names and dimensions by variable name
        if len(variables_name) > 1:
            variables_name, dimensions = zip(
                *sorted(zip(variables_name, dimensions), key=lambda x: x[0])
            )

        space = Space(dimensions)
        return cls(tuple(variables_name), space)

    @property
    def as_yaml(self) -> dict:
        yaml = {
            "sided": {
                "_".join(variable_name.split("_")[:-1]): {
                    "low": dimension.low,
                    "high": dimension.high,
                    "prior": dimension.prior,
                    "base": dimension.base,
                }
                for variable_name, dimension in zip(
                    self.variables_name, self.space.dimensions
                )
                if variable_name.endswith("_BUY") or variable_name.endswith("_SELL")
            },
            "not_sided": {
                variable_name: {
                    "low": dimension.low,
                    "high": dimension.high,
                    "prior": dimension.prior,
                    "base": dimension.base,
                }
                for variable_name, dimension in zip(
                    self.variables_name, self.space.dimensions
                )
                if not variable_name.endswith("_BUY")
                and not variable_name.endswith("_SELL")
            },
        }
        # do not include empty sections
        if yaml["sided"] == {}:
            del yaml["sided"]
        if yaml["not_sided"] == {}:
            del yaml["not_sided"]
        return yaml
