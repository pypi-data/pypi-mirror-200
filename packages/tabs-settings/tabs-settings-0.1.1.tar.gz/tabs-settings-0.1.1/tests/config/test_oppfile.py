import pytest

from tabs_settings.config.oppfile import OppfileConfig


@pytest.fixture
def oppfile_yaml():
    return {
        "signal_builder": {
            "windows_size": [10, 50, 260, 500, 1000, 2000],
            "levels": [0, 1, 2, 3],
        },
        "deadspaces": ["1ms"],
        "fillsims": ["10ms"],
        "horizons": ["100ms", "1s"],
        "fees": [0, 0.0004],
    }


def test_oppfile_config_yaml_round_trip(oppfile_yaml):
    oppfile = OppfileConfig.from_yaml(oppfile_yaml)
    assert oppfile.as_yaml == oppfile_yaml
