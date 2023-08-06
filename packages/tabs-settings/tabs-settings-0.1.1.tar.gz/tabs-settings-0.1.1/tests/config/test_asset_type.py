import pytest

from tabs_settings.config.asset_type import AssetType


@pytest.mark.parametrize(
    "asset_type, expected",
    [
        ("spot", AssetType.SPOT),
        ("future", AssetType.FUTURE),
        ("option", AssetType.OPTION),
    ],
)
def test_asset_type_from_settings(asset_type, expected) -> None:
    assert AssetType.from_settings(asset_type) == expected


@pytest.mark.parametrize(
    "asset_type, expected",
    [
        (AssetType.SPOT, "spot"),
        (AssetType.FUTURE, "future"),
        (AssetType.OPTION, "option"),
    ],
)
def test_asset_type_str(asset_type: AssetType, expected: str) -> None:
    assert str(asset_type) == expected
