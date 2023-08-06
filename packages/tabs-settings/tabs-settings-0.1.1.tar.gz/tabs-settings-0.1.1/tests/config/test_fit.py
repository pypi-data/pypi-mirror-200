from tabs_settings.config.fit import FitConfig
from tabs_settings.config.horizon import Horizon


def test_fit_config_from_yaml():
    yaml_dict = {
        "model_params": {
            "n_estimators": 100,
            "max_depth": 3,
            "random_state": 0,
        },
        "pca_params": {
            "n_components": 0.95,
        },
        "horizons": [
            "10s",
            "30s",
            "1m",
        ],
    }
    assert FitConfig.from_yaml(yaml_dict) == FitConfig(
        model_params=yaml_dict["model_params"],
        pca_params=yaml_dict["pca_params"],
        horizons=(tuple([Horizon("10s"), Horizon("30s"), Horizon("1m")])),
    )
