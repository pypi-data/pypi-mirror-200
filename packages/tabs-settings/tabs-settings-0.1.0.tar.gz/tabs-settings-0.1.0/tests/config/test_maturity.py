import pytest

from tabs_settings.config.maturity import Maturity


@pytest.mark.parametrize(
    "maturity, expected",
    [
        (None, Maturity()),
        ("20220325", Maturity("20220325")),
        ("20220326", ValueError),
        ("20220331", ValueError),
        ("20220429", Maturity("20220429")),
        ("20220430", ValueError),
        ("20220527", Maturity("20220527")),
        ("20220528", ValueError),
        ("20220624", Maturity("20220624")),
        ("20220625", ValueError),
    ],
)
def test_maturity_from_settings(maturity, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            Maturity.from_settings(maturity)
    else:
        assert Maturity.from_settings(maturity) == expected
        assert Maturity.from_settings(maturity) == expected


@pytest.mark.parametrize(
    "maturity, expected",
    [
        (Maturity(), None),
        (Maturity("20230331"), "230331"),
    ],
)
def test_maturity_exchange_name(maturity, expected):
    assert maturity.exchange_name == expected


def test_is_perpetual():
    assert Maturity().is_perpetual
    assert not Maturity("20230331").is_perpetual


def test_maturity_name():
    assert Maturity().name is None
    assert Maturity("20230331").name == "20230331"
