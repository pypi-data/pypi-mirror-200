from tabs_settings.config.stochastic_optimization import StochasticOptimizationConfig


def test_stochastic_optimization_round_trip():
    settings = {
        "objective": {},
        "dimensions": {
            "horizons": ["1m", "5m", "10m"],
            "fee": [0],
        },
        "n_iterations": 110,
        "optimizer_settings": {
            "base_estimator": "gp",
            "n_initial_points": 100,
        },
        "search_space": {
            "sided": {
                "quantile": {
                    "low": 0.00001,
                    "high": 0.1,
                    "prior": "log-uniform",
                    "base": 10,
                }
            }
        },
    }
    assert StochasticOptimizationConfig.from_yaml(settings).as_yaml == settings
