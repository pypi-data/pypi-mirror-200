from tabs_settings.config.signal_builder import SignalBuilderConfig


def test_signal_builder_config_from_yaml():
    assert SignalBuilderConfig.from_yaml(
        {"windows_size": [10, 50], "levels": [0, 1]}
    ) == SignalBuilderConfig(windows_size=tuple([10, 50]), levels=tuple([0, 1]))


def test_signal_builder_config_as_yaml():
    assert SignalBuilderConfig.from_yaml(
        {"windows_size": [10, 50], "levels": [0, 1]}
    ).as_yaml == {
        "windows_size": [10, 50],
        "levels": [
            0,
            1,
        ],
    }
