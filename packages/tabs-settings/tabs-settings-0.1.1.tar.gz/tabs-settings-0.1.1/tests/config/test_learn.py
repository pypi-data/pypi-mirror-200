from tabs_settings.config.learn import LearnConfig


def test_learn_config_yaml_round_trip(learn_yaml):
    learn = LearnConfig.from_yaml(learn_yaml)
    assert learn.as_yaml == learn_yaml


def test_learn_name(learn_yaml):
    learn = LearnConfig.from_yaml(learn_yaml)
    assert learn.name == "test_roll/ETHUSDT-ADAUSDT-20220420_40"


def test_settings_check(learn_yaml):
    learn = LearnConfig.from_yaml(learn_yaml)
    learn._settings_check()
