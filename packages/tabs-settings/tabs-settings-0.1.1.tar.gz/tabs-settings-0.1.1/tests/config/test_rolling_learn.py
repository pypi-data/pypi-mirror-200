from tabs_settings.config.rolling_learn import RollingLearnConfig

SEED = 0


def test_rolling_learn_config_yaml_round_trip(rolling_learn_yaml):
    rolling_learn = RollingLearnConfig.from_yaml(rolling_learn_yaml)
    assert rolling_learn.as_yaml == rolling_learn_yaml


# def test_rolling_learn_name(rolling_learn_yaml):
#     rolling_learn = RollingLearn.from_yaml(rolling_learn_yaml)
#     assert rolling_learn.name == ""
