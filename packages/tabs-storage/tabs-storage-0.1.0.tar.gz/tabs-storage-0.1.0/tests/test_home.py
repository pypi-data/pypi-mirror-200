from pathlib import Path

import pytest

from tabs_storage.home import Home, HomeType


@pytest.mark.parametrize(
    "home_type_str, path, expected_type",
    [
        ("local", None, HomeType.LOCAL),
        ("hdd", None, HomeType.HDD),
        ("google", None, HomeType.GOOGLE),
        ("test", Path("test"), HomeType.TEST),
    ],
)
def test_home_path_from_settings(home_type_str, path, expected_type):
    home = Home.from_settings(home_type_str, path)
    assert home._type == expected_type
